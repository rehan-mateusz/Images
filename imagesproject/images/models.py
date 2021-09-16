from datetime import datetime
from datetime import timezone

from django.db import models

from imagesproject import settings

User = settings.AUTH_USER_MODEL


class Image(models.Model):
    img = models.ImageField()
    owner = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)


class Thumbnail(models.Model):
    original = models.ForeignKey(Image, blank=True, on_delete=models.CASCADE)
    height = models.IntegerField()
    width = models.IntegerField()
    thumbnail = models.ImageField()

class TempURL(models.Model):
    id = models.CharField(primary_key=True, editable=False, max_length=32)
    data = models.JSONField()
    valid_until = models.DateTimeField()

    def is_active(self):
        return datetime.now(timezone.utc) <= self.valid_until
