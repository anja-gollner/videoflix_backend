from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from video_app.models import Video, UserVideoProgress
from video_app.api.serializers import VideoSerializer, UserVideoProgressSerializer
from datetime import datetime
from django.core.files.uploadedfile import SimpleUploadedFile

dummy_file = SimpleUploadedFile(
    "video.mp4", b"dummy content", content_type="video/mp4")


class VideoSerializerTestCase(APITestCase):
    def setUp(self):
        """Vorbereitungen für die Tests"""
        self.valid_data = {
            "title": "Test Video",
            "description": "Dies ist ein Testvideo",
            "category": "action",
            "video_file": dummy_file
        }
        self.video = Video.objects.create(**self.valid_data)

    def test_valid_data(self):
        """Test für gültige Daten"""
        serializer = VideoSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_missing_title(self):
        """Test für fehlenden Titel"""
        data = self.valid_data.copy()
        del data["title"]
        serializer = VideoSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)

    def test_missing_video_file(self):
        """Test für fehlende Videodatei"""
        data = self.valid_data.copy()
        del data["video_file"]
        serializer = VideoSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("video_file", serializer.errors)

    def test_read_only_fields(self):
        """Test für schreibgeschützte Felder"""
        data = self.valid_data.copy()
        data["thumbnail"] = "path/to/thumbnail.jpg"
        data["video_720p"] = "path/to/video_720p.mp4"
        serializer = VideoSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertNotIn("thumbnail", serializer.validated_data)
        self.assertNotIn("video_720p", serializer.validated_data)

    def test_create_video(self):
        """Test für das Erstellen eines neuen Videos"""
        serializer = VideoSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        video = serializer.save()
        self.assertEqual(video.title, "Test Video")
        self.assertEqual(video.description, "Dies ist ein Testvideo")


class UserVideoProgressSerializerTestCase(APITestCase):
    def setUp(self):
        """Vorbereitungen für die Tests"""
        self.user = User.objects.create_user(
            username="testuser", password="password123")
        self.video = Video.objects.create(
            title="Test Video",
            description="Test Video Beschreibung",
            category="action",
            video_file=dummy_file
        )
        self.valid_data = {
            "video": self.video.id,
            "last_viewed_position": 10.5,
            "viewed": False,
            "last_viewed_at": datetime.now().isoformat()
        }
        self.factory = APIRequestFactory()
        self.request = self.factory.post("/progress/", self.valid_data)
        self.request.user = self.user

    def test_valid_data(self):
        """Test für gültige Daten"""
        serializer = UserVideoProgressSerializer(
            data=self.valid_data, context={"request": self.request})
        self.assertTrue(serializer.is_valid())

    def test_missing_video(self):
        """Test für fehlendes Video"""
        data = self.valid_data.copy()
        del data["video"]
        serializer = UserVideoProgressSerializer(
            data=data, context={"request": self.request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("video", serializer.errors)

    def test_user_read_only(self):
        """Test, dass das user-Feld schreibgeschützt ist"""
        data = self.valid_data.copy()
        data["user"] = 999
        serializer = UserVideoProgressSerializer(
            data=data, context={"request": self.request})
        self.assertTrue(serializer.is_valid())
        self.assertNotIn("user", serializer.validated_data)

    def test_update_progress(self):
        """Test für das Aktualisieren eines Fortschritts"""
        progress = UserVideoProgress.objects.create(
            user=self.user, video=self.video, last_viewed_position=10.5
        )
        update_data = {
            "last_viewed_position": 20.0,
            "viewed": True
        }
        serializer = UserVideoProgressSerializer(
            instance=progress, data=update_data, context={"request": self.request}, partial=True
        )
        self.assertTrue(serializer.is_valid())
        updated_progress = serializer.save()
        self.assertEqual(updated_progress.last_viewed_position, 20.0)
        self.assertTrue(updated_progress.viewed)
        self.assertEqual(updated_progress.user, self.user)
