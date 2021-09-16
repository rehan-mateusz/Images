import json
import io

from PIL import Image as PilImage
from PIL import ImageOps

from rest_framework import serializers
from django.core.files.uploadedfile import InMemoryUploadedFile

from . import models
from accounts import models as accmodels

class ThumbnailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Thumbnail
        fields = ('thumbnail', 'height', 'width')


class ImageSerializer(serializers.ModelSerializer):
    image_name = serializers.SerializerMethodField()

    class Meta:
        model = models.Image
        fields = ('image_name', 'id', 'img')

    def get_image_name(self, image):
        return image.img.name

    def create(self, validated_data):
        new_image = models.Image.objects.create(
            img = validated_data['img'],
            owner = validated_data['user'])
        sizes = json.loads(validated_data['user'].plan.thumbnails_sizes['sizes'])
        create_thumbnails(new_image, sizes)
        return new_image

    def to_representation(self, instance):
        instance = super().to_representation(instance)
        if self.context['request'].method == 'GET':
            instance.pop('img')
        return instance

class ImageRetrieveSerializer(serializers.ModelSerializer):
    thumbnails = ThumbnailSerializer(read_only=True, many=True, source='thumbnail_set')

    class Meta:
        model = models.Image
        fields = ('img', 'thumbnails', 'id')

    def to_representation(self, instance):
        instance = super().to_representation(instance)
        if not self.context['request'].user.plan.has_original:
            instance.pop('img')
        return instance


class TempURLSerializer(serializers.ModelSerializer):
    image_data = serializers.SerializerMethodField()

    class Meta:
        model = models.TempURL
        fields = ('image_data',)

    def get_image_data(self, temp_url):
        if temp_url.is_active():
            return json.loads(temp_url.data)
        return 'Link has expired'


def create_thumbnails(base_image, sizes):
    image = PilImage.open(base_image.img.path)
    for size in sizes:
        size = clean_size(image.size, size)
        thumb_file = prepare_thumbnail(image, size, base_image.img.name)
        new_thumb = models.Thumbnail.objects.create(
            thumbnail = thumb_file,
            width = size[0],
            height = size[1],
            original = base_image)

def clean_size(img_size, thumb_size):
    if thumb_size[0] == 0:
        thumb_size[0] = img_size[0]
    if thumb_size[1] == 0:
        thumb_size[1] = img_size[1]
    return thumb_size

def prepare_thumbnail(image, size, base_img_name):
    transposed_img = ImageOps.exif_transpose(image)
    resized_img = transposed_img.resize(size)
    thumb_io = io.BytesIO()
    resized_img.save(thumb_io, format=image.format)
    img_name = '{}_thmb{}x{}.{}'.format(base_img_name, size[0],
        size[1], image.format)
    thumb_file = InMemoryUploadedFile(thumb_io, None, img_name,
                                      'image/jpeg', thumb_io.tell, None)
    return thumb_file
