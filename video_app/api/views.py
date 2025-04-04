
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework import generics
from .serializers import UserVideoProgressSerializer, VideoSerializer
from video_app.models import Video, UserVideoProgress
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


# @method_decorator(cache_page(CACHE_TTL), name='dispatch')
class VideoListView(generics.ListCreateAPIView):
    queryset = Video.objects.all().order_by('-created_at')
    serializer_class = VideoSerializer


class VideoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class UserVideoProgressListView(generics.ListCreateAPIView):
    serializer_class = UserVideoProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = UserVideoProgress.objects.filter(user=self.request.user)
        video_id = self.request.query_params.get('video')
        if video_id:
            queryset = queryset.filter(video__id=video_id)
        return queryset

    def perform_create(self, serializer):
        video_id = self.request.data.get('video')
        video = get_object_or_404(Video, pk=video_id)

        user = self.request.user
        if not UserVideoProgress.objects.filter(user=user, video=video).exists():
            serializer.save(user=user)
        else:
            progress = UserVideoProgress.objects.get(user=user, video=video)
            progress.last_viewed_position = self.request.data.get(
                'last_viewed_position')
            progress.viewed = self.request.data.get('viewed')
            progress.save()


class UserVideoProgressDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserVideoProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserVideoProgress.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied(
                "Du kannst nur deinen eigenen Fortschritt aktualisieren.")
        serializer.save()
