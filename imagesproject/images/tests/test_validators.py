import pytest

from datetime import datetime
from datetime import timezone
from datetime import timedelta

from images.validators import valid_until_validator


def test_valid_until_validator_valid_data():
    value = datetime.now(timezone.utc) + timedelta(seconds=60)
    try:
        valid_until_validator(value)
        validated = True
    except:
        validated = False
    assert validated

@pytest.mark.parametrize(
    'secs',
    [20, 40000])
def test_valid_until_validator_invalid_data(secs):
    value = datetime.now(timezone.utc) + timedelta(seconds=secs)
    try:
        valid_until_validator(value)
        validated = False
    except:
        validated = True
    assert validated
