from rest_framework import serializers
from video_app.models import Video, UserVideoProgress
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

        read_only_fields = ['thumbnail',
                            'video_120p', 'video_360p', 'video_720p', 'video_1080p']


class UserVideoProgressSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    permission_classes = [IsAuthenticated]

    class Meta:
        model = UserVideoProgress
        fields = ['id', 'user', 'video',
                  'last_viewed_position', 'viewed', 'last_viewed_at']

    # def create(self, validated_data):
    #     user = self.context['request'].user
    #     video_id = self.context['request'].data.get('video')
    #     video = get_object_or_404(Video, pk=video_id)
    #     return UserVideoProgress.objects.create(user=user, video=video, **validated_data)

    # def update(self, instance, validated_data):
    #     validated_data['user'] = self.context['request'].user
    #     return super().update(instance, validated_data)
