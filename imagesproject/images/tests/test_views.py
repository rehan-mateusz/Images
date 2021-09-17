import tempfile
import json
import shutil

from io import BytesIO
from PIL import Image as PilImage

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework import status

from django.test import override_settings
from django.urls import reverse
from django.core.files import File

from accounts.models import Account
from accounts.models import Plan
from images.models import Image
from images.models import Thumbnail
from images.models import TempURL
from images import views


MEDIA_ROOT = tempfile.mkdtemp()

@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class ViewsTestCase(APITestCase):

    def setUp(self):
        self.plan1 = Plan.objects.create(
            name = 'test_plan1',
            thumbnails_sizes = {'sizes': '[[100, 100], [200, 200]]'},
            can_share = True,
            has_original = True,
        )
        self.user1 = Account(
            email = 'testemail@email.com',
            username = 'test1',
            password = 'psw1',
            plan = self.plan1)
        self.user1.save()
        self.user2 = Account(
            email = 'testemail2@email.com',
            username = 'test2',
            password = 'psw2',
            plan = self.plan1)
        self.user2.save()
        self.image1 = Image(
            owner=self.user1
        )
        self.image1.save()

    @classmethod
    def tearDownClass(self):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def get_image_file(self, name):
        file = BytesIO()
        image = PilImage.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = name
        file.seek(0)
        return file


    def test_ImageListCreateView_GET_nologin(self):
        response = self.client.get(reverse('images:list_create'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_ImageListCreateView_GET_with_login(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(reverse('images:list_create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ImageListCreateView_POST_creates_image_with_thumbnails(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(
            reverse('images:list_create'),
            data={'img': self.get_image_file('test.png')},
            format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Image.objects.filter(owner=self.user1))
        self.assertTrue(Thumbnail.objects.filter(
            original=Image.objects.filter(owner=self.user1).last()).count()==2)

    def test_ImageRetriveAPIView_GET_with_login(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(reverse('images:img_details',
            kwargs={'pk': self.image1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ImageRetriveAPIView_GET_with_not_owner(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(reverse('images:img_details',
            kwargs={'pk': self.image1.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_TempURLCreateView_creates_TempURL(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(reverse('images:create_temp',
            kwargs={'pk': self.image1.id, 'seconds': 45}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_TempURLView_get(self):
        response = self.client.get(reverse('images:temp_url',
            kwargs={'pk': 'random'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
