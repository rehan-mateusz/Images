<<<<<<< Updated upstream
from django.shortcuts import render

# Create your views here.
=======
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from . import serializers

class ImageListCreateView(generics.ListCreateAPIView):
    serializer_class = serializers.ImageSerializer
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
>>>>>>> Stashed changes
