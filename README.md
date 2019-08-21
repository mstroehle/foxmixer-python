# Python 3 library for https://www.foxmixer.com / http://foxmixer6mrsuxrl.onion
## Bitcoin mixer/tumbler

## Installation

* `pip3 install foxmixer || pip install foxmixer`

## Usage

* `foxmixer mix --currency bitcoin --address 1a....`
* Make sure a Tor SOCKS proxy is running locally (127.0.0.1:9050)

If you have a mixcode from a previous mix:

* `foxmixer mix --currency bitcoin --address 1a.... --mixcode ....`

## Note

This does take an affiliate-style "fee" by default. You can override this if you don't want to pay it.

## Screenshot

![foxmixer CLI screenshot](https://pic8.co/sh/bJtKdm.png)

# Licence

[Unlicense/Public domain](LICENSE.txt)
