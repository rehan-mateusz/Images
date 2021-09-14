from rest_framework import serializers

from . import models


class ThumbnailSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('thumbnail',)


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('image',)
