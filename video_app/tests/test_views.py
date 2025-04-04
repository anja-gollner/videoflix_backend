from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from video_app.models import Video, UserVideoProgress
from django.core.files.uploadedfile import SimpleUploadedFile


class VideoListViewTestCase(APITestCase):
    def setUp(self):
        """Vorbereitungen für die Tests"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="password123")
        self.video1 = Video.objects.create(
            title="Video 1", description="Beschreibung 1", category="action", video_file="path/to/video1.mp4")
        self.video2 = Video.objects.create(
            title="Video 2", description="Beschreibung 2", category="comedy", video_file="path/to/video2.mp4")

    def test_get_video_list(self):
        """Test für das Abrufen der Videoliste"""
        response = self.client.get(reverse('video-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_video_authenticated(self):
        self.client.force_authenticate(user=self.user)
        video_file = SimpleUploadedFile(
            "video.mp4", b"file_content", content_type="video/mp4")
        data = {
            "title": "Neues Video",
            "description": "Neue Beschreibung",
            "category": "action",
            "video_file": video_file
        }
        response = self.client.post(
            reverse('video-list'), data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_video_unauthenticated(self):
        """Test für das Erstellen eines Videos ohne Authentifizierung"""
        data = {
            "title": "Neues Video",
            "description": "Neue Beschreibung",
            "category": "action",
            "video_file": "path/to/new_video.mp4"
        }
        response = self.client.post(reverse('video-list'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class VideoDetailViewTestCase(APITestCase):
    def setUp(self):
        """Vorbereitungen für die Tests"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="password123")
        self.video = Video.objects.create(
            title="Test Video", description="Beschreibung", category="action", video_file="path/to/video.mp4")

    def test_get_video_detail(self):
        """Test für das Abrufen eines einzelnen Videos"""
        response = self.client.get(
            reverse('video-detail', kwargs={'pk': self.video.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Test Video")

    def test_update_video_authenticated(self):
        """Test für das Aktualisieren eines Videos als authentifizierter Benutzer"""
        self.client.force_authenticate(user=self.user)
        data = {"title": "Aktualisiertes Video"}
        response = self.client.patch(
            reverse('video-detail', kwargs={'pk': self.video.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.video.refresh_from_db()
        self.assertEqual(self.video.title, "Aktualisiertes Video")

    def test_delete_video_authenticated(self):
        """Test für das Löschen eines Videos als authentifizierter Benutzer"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            reverse('video-detail', kwargs={'pk': self.video.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Video.objects.filter(pk=self.video.pk).exists())

    def test_update_video_unauthenticated(self):
        """Test für das Aktualisieren eines Videos ohne Authentifizierung"""
        data = {"title": "Aktualisiertes Video"}
        response = self.client.patch(
            reverse('video-detail', kwargs={'pk': self.video.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserVideoProgressListViewTestCase(APITestCase):
    def setUp(self):
        """Vorbereitungen für die Tests"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="password123")
        self.video = Video.objects.create(
            title="Test Video", description="Beschreibung", category="action", video_file="path/to/video.mp4")
        self.client.force_authenticate(user=self.user)

    def test_get_progress_list(self):
        """Test für das Abrufen der Fortschrittsliste"""
        UserVideoProgress.objects.create(
            user=self.user, video=self.video, last_viewed_position=10.5)
        response = self.client.get(reverse('progress-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_progress_list_filtered_by_video(self):
        """Test für das Abrufen der Fortschrittsliste mit Video-Filter"""
        UserVideoProgress.objects.create(
            user=self.user, video=self.video, last_viewed_position=10.5)
        response = self.client.get(
            reverse('progress-list'), {'video': self.video.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['video'], self.video.id)

    def test_create_progress(self):
        """Test für das Erstellen eines neuen Fortschritts"""
        data = {
            "video": self.video.id,
            "last_viewed_position": 5.0,
            "viewed": False
        }
        response = self.client.post(reverse('progress-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserVideoProgress.objects.count(), 1)
        self.assertEqual(
            UserVideoProgress.objects.first().last_viewed_position, 5.0)

    def test_update_existing_progress(self):
        """Test für das Aktualisieren eines bestehenden Fortschritts"""
        progress = UserVideoProgress.objects.create(
            user=self.user, video=self.video, last_viewed_position=10.5)
        data = {
            "video": self.video.id,
            "last_viewed_position": 30.0,
            "viewed": True
        }
        response = self.client.post(reverse('progress-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        progress.refresh_from_db()
        self.assertEqual(progress.last_viewed_position, 30.0)
        self.assertTrue(progress.viewed)

    def test_get_progress_list_unauthenticated(self):
        """Test für das Abrufen der Fortschrittsliste ohne Authentifizierung"""
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('progress-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserVideoProgressDetailViewTestCase(APITestCase):
    def setUp(self):
        """Vorbereitungen für die Tests"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="password123")
        self.video = Video.objects.create(
            title="Test Video", description="Beschreibung", category="action", video_file="path/to/video.mp4")
        self.progress = UserVideoProgress.objects.create(
            user=self.user, video=self.video, last_viewed_position=10.5)
        self.client.force_authenticate(user=self.user)

    def test_get_progress_detail(self):
        """Test für das Abrufen eines einzelnen Fortschritts"""
        response = self.client.get(
            reverse('progress-detail', kwargs={'pk': self.progress.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['last_viewed_position']), 10.5)

    def test_update_progress(self):
        """Test für das Aktualisieren eines Fortschritts"""
        data = {"last_viewed_position": 20.0, "viewed": True}
        response = self.client.patch(
            reverse('progress-detail', kwargs={'pk': self.progress.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.progress.refresh_from_db()
        self.assertEqual(self.progress.last_viewed_position, 20.0)
        self.assertTrue(self.progress.viewed)

    def test_delete_progress(self):
        """Test für das Löschen eines Fortschritts"""
        response = self.client.delete(
            reverse('progress-detail', kwargs={'pk': self.progress.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(UserVideoProgress.objects.filter(
            pk=self.progress.pk).exists())

    def test_update_other_user_progress(self):
        """Test für den Versuch, den Fortschritt eines anderen Benutzers zu aktualisieren"""
        other_user = User.objects.create_user(
            username="otheruser", password="password123")
        other_progress = UserVideoProgress.objects.create(
            user=other_user, video=self.video, last_viewed_position=15.0)
        data = {"last_viewed_position": 25.0}
        response = self.client.patch(
            reverse('progress-detail', kwargs={'pk': other_progress.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_progress_detail_unauthenticated(self):
        """Test für das Abrufen eines Fortschritts ohne Authentifizierung"""
        self.client.force_authenticate(user=None)
        response = self.client.get(
            reverse('progress-detail', kwargs={'pk': self.progress.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
