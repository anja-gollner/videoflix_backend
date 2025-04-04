from datetime import date
from django.db import models
from moviepy import VideoFileClip
from django.core.files.uploadedfile import InMemoryUploadedFile
import io
from django.core.files import File
from PIL import Image
from django.contrib.auth.models import User


class Video(models.Model):
    CATEGORY_CHOICES = (
        ('fantasy', 'fantasy'),
        ('action', 'action'),
        ('romantic', 'romantic'),
        ('documentary', 'documentary'),
        ('comedy', 'comedy'),
    )

    title = models.CharField(max_length=80)
    description = models.CharField(max_length=500)
    video_file = models.FileField(upload_to='videos', null=False, blank=False)
    thumbnail = models.ImageField(
        upload_to='thumbnails/', null=True, blank=True)
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    video_120p = models.FileField(
        upload_to='videos/120p/', null=True, blank=True, max_length=255)
    video_360p = models.FileField(
        upload_to='videos/360p/', null=True, blank=True, max_length=255)
    video_720p = models.FileField(
        upload_to='videos/720p/', null=True, blank=True, max_length=255)
    video_1080p = models.FileField(
        upload_to='videos/1080p/', null=True, blank=True, max_length=255)

    def __str__(self):
        return self.title


class UserVideoProgress(models.Model):
    user = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name='watched_videos')
    video = models.ForeignKey(
        Video, on_delete=models.CASCADE, related_name='watchers')
    last_viewed_position = models.FloatField(default=0.0)
    viewed = models.BooleanField(default=False)
    last_viewed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "video")

    def __str__(self):
        return f"{self.user.username} - {self.video.title}"
