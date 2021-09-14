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
