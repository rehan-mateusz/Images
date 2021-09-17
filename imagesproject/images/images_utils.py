import io

from PIL import Image as PilImage
from PIL import ImageOps

from django.core.files.uploadedfile import InMemoryUploadedFile

from . import models


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
