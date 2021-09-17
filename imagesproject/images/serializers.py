import json

from rest_framework import serializers

from . import models
from . import images_utils
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
        images_utils.create_thumbnails(new_image, sizes)
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
