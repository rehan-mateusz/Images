import secrets
import json

from datetime import datetime
from datetime import timedelta

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import serializers
from . import models


class ImageListCreateView(generics.ListCreateAPIView):
    serializer_class = serializers.ImageSerializer
    permission_classes = [IsAuthenticated]
    queryset = models.Image.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request):
        queryset = self.get_queryset()
        if self.request.user.plan.has_original:
            queryset = queryset.filter(owner=self.request.user)
            serializer = serializers.ImageSerializer(queryset, many=True,
                context = self.get_serializer_context())
        return Response(serializer.data)


class ImageRetriveAPIView(generics.RetrieveAPIView):
    # permission_classes = owner
    serializer_class = serializers.ImageRetrieveSerializer
    queryset = models.Image.objects.all()


class TempURLCreateView(generics.RetrieveAPIView):
    # permission_classes = owner and can_link
    serializer_class = serializers.ImageRetrieveSerializer
    queryset = models.Image.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        url = models.TempURL.objects.create(
            id = secrets.token_urlsafe(32),
            data = json.dumps(dict(serializer.data)),
            valid_until = datetime.now() + timedelta(seconds=self.kwargs['seconds']))
        return Response(url.id)

class TempURLView(generics.RetrieveAPIView):
    serializer_class = serializers.TempURLSerializer
    queryset = models.Image.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = models.TempURL.objects.filter(id=self.kwargs['pk'])
        if instance.count() == 0:
            return Response('No Image Avaliable!')
        serializer = self.get_serializer(instance)
        return Response(serializer.data['image_data'])
