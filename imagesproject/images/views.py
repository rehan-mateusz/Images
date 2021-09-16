from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import serializers
from . import models


class ImageListCreateView(generics.ListCreateAPIView):
    serializer_class = serializers.ImageSerializer
    # permission_classes = [IsAuthenticated]
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

class ImageRetriveAPIVIew(generics.RetrieveAPIView):
    serializer_class = serializers.ImageRetrieveSerializer
    queryset = models.Image.objects.all()
