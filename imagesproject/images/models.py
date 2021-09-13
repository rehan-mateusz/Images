from django.db import models

from imagesproject import settings

User = settings.AUTH_USER_MODEL


class Thumbnail(models.Model):
    original = models.ForeignKey(Image, on_delete=models.CASCADE)
    height = models.IntegerField()
    width = models.IntegerField()
    img = models.ImageField()


class Image(models.Model):
    img = models.ImageField()
    owner = ForeignKey(User, on_delete=models.CASCADE)
