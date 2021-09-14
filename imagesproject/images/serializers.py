import json
import io

from PIL import Image as PilImage

from rest_framework import serializers
from django.core.files.uploadedfile import InMemoryUploadedFile

from . import models
from accounts import models as accmodels

class ThumbnailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Thumbnail
        fields = ('thumbnail', 'height', 'width')


class ImageSerializer(serializers.ModelSerializer):
    thumbnails = ThumbnailSerializer(read_only=True, many=True, source='thumbnail_set')

    class Meta:
        model = models.Image
        fields = ('img', 'thumbnails')

    def create(self, validated_data):
        new_image = models.Image.objects.create(
            img = validated_data['img'],
            owner = validated_data['user'])
        sizes = json.loads(validated_data['user'].plan.thumbnails_sizes['sizes'])
        create_thumbnails(new_image, sizes)
        return new_image


def create_thumbnails(base_image, sizes):
    for size in sizes:
        thumb_io = io.BytesIO()
        image = PilImage.open(base_image.img.path)
        image.thumbnail(size)
        image.save(thumb_io, format=image.format)
        img_name = '{}_thmb{}x{}.{}'.format(
            base_image.img.name,
            size[0],
            size[1],
            image.format)
        thumb_file = InMemoryUploadedFile(thumb_io, None, img_name,
                                          'image/jpeg', thumb_io.tell, None)
        new_thumb = models.Thumbnail.objects.create(
            thumbnail = thumb_file,
            width = size[0],
            height = size[1],
            original = base_image)
