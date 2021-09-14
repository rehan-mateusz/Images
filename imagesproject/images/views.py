from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from . import serializers
from . import models


class ImageListCreateView(generics.ListCreateAPIView):
    serializer_class = serializers.ImageSerializer
    # permission_classes = [IsAuthenticated]
    queryset = models.Image.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
