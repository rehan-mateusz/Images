import secrets
import json

from datetime import datetime
from datetime import timedelta
from datetime import timezone

from django.core.exceptions import ValidationError
from django.urls import reverse

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from . import permissions
from . import serializers
from . import models


class ImageListCreateView(generics.ListCreateAPIView):
    serializer_class = serializers.ImageSerializer
    permission_classes = [IsAuthenticated, ]
    queryset = models.Image.objects.all()


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = {'id': serializer.data['id']}
        headers = self.get_success_headers(data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = serializers.ImageSerializer(
            queryset, many=True, context=self.get_serializer_context())
        return Response(serializer.data)


class ImageRetriveAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsImageOwner, ]
    serializer_class = serializers.ImageRetrieveSerializer
    queryset = models.Image.objects.all()


class TempURLCreateView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsImageOwnerAndCanLink, ]
    serializer_class = serializers.ImageRetrieveSerializer
    queryset = models.Image.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        url = models.TempURL(
            id=secrets.token_urlsafe(32),
            data=json.dumps(dict(serializer.data)),
            valid_until=datetime.now(timezone.utc) + timedelta(
                seconds=self.kwargs['seconds']))
        try:
            url.full_clean()
            url.save()
        except ValidationError:
            return Response('Link can be valid between 30 and 30000 seconds')
        return Response(self.request.build_absolute_uri(
            reverse('images:temp_url', kwargs={'pk': url.id})))


class TempURLView(generics.RetrieveAPIView):
    serializer_class = serializers.TempURLSerializer
    queryset = models.Image.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = models.TempURL.objects.filter(id=self.kwargs['pk'])
        if not instance.exists():
            return Response('No Image Avaliable!')
        serializer = self.get_serializer(instance.first())
        return Response(serializer.data['image_data'])
