from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class RegistrationViewTestCase(APITestCase):

    def setUp(self):
        """ Vorbereitungen für Tests """
        self.url = reverse('registration')

    def test_successful_registration(self):
        """ Test für erfolgreiche Registrierung """
        data = {
            "email": "testuser@example.com",
            "password": "password123",
            "repeated_password": "password123"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertIn('user_id', response.data)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'], data['email'])
        user = User.objects.get(id=response.data['user_id'])
        self.assertEqual(user.email, data['email'])

    def test_email_already_exists(self):
        """ Test für E-Mail-Adresse, die bereits verwendet wird """
        User.objects.create_user(
            email='existing@example.com', username='existing', password='password123')

        data = {
            "email": "existing@example.com",
            "password": "password123",
            "repeated_password": "password123"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(
            response.data['email'][0], "Diese E-Mail-Adresse wird bereits verwendet.")

    def test_password_mismatch(self):
        """ Test für nicht übereinstimmende Passwörter """
        data = {
            "email": "testuser@example.com",
            "password": "password123",
            "repeated_password": "password456"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('repeated_password', response.data)
        self.assertEqual(
            response.data['repeated_password'][0], "Die Passwörter stimmen nicht überein.")

    def test_missing_email(self):
        """ Test für fehlende E-Mail-Adresse """
        data = {
            "password": "password123",
            "repeated_password": "password123"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_missing_password(self):
        """ Test für fehlendes Passwort """
        data = {
            "email": "testuser@example.com",
            "repeated_password": "password123"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_missing_repeated_password(self):
        """ Test für fehlendes wiederholtes Passwort """
        data = {
            "email": "testuser@example.com",
            "password": "password123",
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('repeated_password', response.data)

    def test_short_password(self):
        """ Test für ein zu kurzes Passwort """
        data = {
            "email": "testuser@example.com",
            "password": "short",
            "repeated_password": "short"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
