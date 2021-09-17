from datetime import datetime
from datetime import timezone
from datetime import timedelta

from django.core.exceptions import ValidationError


def valid_until_validator(value):
    min_valid_until = datetime.now(timezone.utc) + timedelta(seconds=29)
    max_valid_until = datetime.now(timezone.utc) + timedelta(seconds=30000)
    if value < min_valid_until or value > max_valid_until:
        raise ValidationError('URL must be valid between 30 and 30000 seconds')
