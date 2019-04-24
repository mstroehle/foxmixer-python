#!/usr/bin/python3

__version__ = '0.0.1'

# API documentation: https://www.foxmixer.com/api

import logging
from time import sleep
from random import randint

import aaargh
import requests
import pyqrcode

from . import validate


CLEARNET_ENDPOINT = 'https://www.foxmixer.com'
TOR_ENDPOINT = 'http://foxmixer6mrsuxrl.onion'

DEFAULT_ENDPOINT = CLEARNET_ENDPOINT

DEFAULT_AFFILIATE = '1CMndA1TgScgKDDnCHYx1ZQDZQJ439ZWpK'

# Fee and delay must be integers, not floats.
# Percentage
DEFAULT_AFFILIATE_FEE = randint(1, 4)

# Hours
DEFAULT_DELAY = randint(2, 3)
DEFAULT_AFFILIATE_DELAY = randint(2, 12)

DEFAULT_TIMEOUT = 60
DEFAULT_RETRY = False

cli = aaargh.App()

logging.basicConfig(level=logging.WARNING)


def api_request(url, get_params=None, retry=False, timeout=DEFAULT_TIMEOUT):
    try:
        request = requests.get(url,
                               params=get_params,
                               timeout=timeout)
    except Exception as e:
        if retry is True:
            logging.warning('Got an error, but retrying: {}'.format(e))
            sleep(5)
            # Try again.
            return api_request(url, get_params=get_params, retry=retry)
        else:
            raise

    status_code_first_digit = request.status_code // 100
    if status_code_first_digit == 2:
        return request.content
    elif status_code_first_digit == 4:
        raise ValueError(request.content)
    elif status_code_first_digit == 5:
        if retry is True:
            logging.warning(request.content)
            logging.warning('Got a 500, retrying in 5 seconds...')
            sleep(5)
            # Try again if we get a 500
            return api_request(url,
                               get_params=get_params,
                               retry=retry,
                               timeout=timeout)
        else:
            raise Exception(request.content)
    else:
        # Not sure why we'd get this.
        request.raise_for_status()
        raise Exception('Stuff broke strangely.')


@cli.cmd(name='mix')
@cli.cmd_arg('--currency', type=str, required=True)
@cli.cmd_arg('--output_address', type=str, required=True)
@cli.cmd_arg('--endpoint', type=str, default=DEFAULT_ENDPOINT)
def _mix_terminal(currency, output_address, endpoint=DEFAULT_ENDPOINT):
    output = mix(currency=currency,
                 output_address=output_address,
                 endpoint=endpoint)
    address = output['address']
    id = output['id']

    uri = '{}:{}'.format(currency, address)
    qr = pyqrcode.create(uri).terminal(module_color='black',
                                       background='white',
                                       quiet_zone=1)
    letter = letter_of_guarantee(id, endpoint=endpoint)
    msg = '{}\n{}\nID: {}\n{}'
    terminal_output = msg.format(qr,
                                 uri,
                                 id,
                                 letter)
    return terminal_output


def mix(currency,
        output_address,
        endpoint=DEFAULT_ENDPOINT,
        delay=DEFAULT_DELAY,
        affiliate=DEFAULT_AFFILIATE,
        affiliate_fee=DEFAULT_AFFILIATE_FEE,
        affiliate_delay=DEFAULT_AFFILIATE_DELAY,
        retry=DEFAULT_RETRY):
    """
    currency must be one of: bitcoin
    output_address is destination for mixed coins.
    affiliate is None or string.
    """
    validate.currency(currency)

    get_params = {'payoutAddress1': output_address,
                  'payoutPercentage1': 100,
                  'payoutDelay1': delay}

    if affiliate is not None:
        get_params['payoutAddress2'] = affiliate
        get_params['payoutPercentage2'] = affiliate_fee
        get_params['payoutDelay2'] = affiliate_delay
        get_params['payoutPercentage1'] = 100 - affiliate_fee

    url = '{}/api/createMix'.format(endpoint)
    output = api_request(url=url, get_params=get_params, retry=retry)
    # Foxmixer replies strangely in a get parameter style.
    output_dict = {}
    output = output.decode('utf-8')
    for item in output.split('&'):
        item_key, item_value = item.split('=')
        output_dict[item_key] = item_value

    final_dict = {'address': output_dict['payinAddress'],
                  'minimum': output_dict['payinAmountMin'],
                  'maximum': output_dict['payinAmountMax'],
                  'id': output_dict['mixId']}
    return final_dict


@cli.cmd
@cli.cmd_arg('id', type=str)
@cli.cmd_arg('--endpoint', type=str, default=DEFAULT_ENDPOINT)
def letter_of_guarantee(id,
                        endpoint=DEFAULT_ENDPOINT,
                        retry=DEFAULT_RETRY):
    """
    Returns the letter of guarantee for a mix.

    Foxmixer is slow on this, if you immediately try to grab
    the letter, it will 404. Hence, the sleep hack.
    """
    sleep(3)
    url = '{}/mix/{}/LetterOfGuarantee.txt'.format(endpoint, id)
    output = api_request(url)
    return output.decode('utf-8')


def main():
    output = cli.run()
    if output is True:
        exit(0)
    elif output is False:
        exit(1)
    else:
        print(output)
        exit(0)


if __name__ == '__main__':
    main
