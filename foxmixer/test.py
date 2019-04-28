import pytest

import foxmixer


def test_mix():
    foxmixer.mix(currency='bitcoin',
                 output_address='1xm4vFerV3pSgvBFkyzLgT1Ew3HQYrS1V',
                 mixcode='Jzvr4')
    with pytest.raises(ValueError):
        foxmixer.mix(currency='bitcoin',
                     output_address='1xm4vFerV3pSgvBFkyzLgT1Ew3HQYrS1V',
                     mixcode='invalidmixcodestring')
    with pytest.raises(ValueError):
        foxmixer.mix(currency='bitcoin',
                     output_address='1invalid')
