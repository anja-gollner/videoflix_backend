from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from user_auth_app.api.serializers import RegistrationSerializer


class RegistrationSerializerTestCase(APITestCase):

    def setUp(self):
        """ Vorbereitungen für Tests """
        self.valid_data = {
            "email": "testuser@example.com",
            "password": "password123",
            "repeated_password": "password123"
        }

    def test_valid_data(self):
        """ Test for valid registration data """
        serializer = RegistrationSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_email(self):
        """ Test for invalid email that already exists """
        User.objects.create_user(
            email='existing@example.com', username='existing', password='password123')

        data = {
            "email": "existing@example.com",
            "password": "password123",
            "repeated_password": "password123"
        }
        serializer = RegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors['email'][0], "Diese E-Mail-Adresse wird bereits verwendet.")

    def test_passwords_mismatch(self):
        """ Test for mismatching passwords """
        data = {
            "email": "testuser@example.com",
            "password": "password123",
            "repeated_password": "password456"
        }
        serializer = RegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors['repeated_password'][0], "Die Passwörter stimmen nicht überein.")

    def test_missing_email(self):
        """ Test for missing email """
        data = {
            "password": "password123",
            "repeated_password": "password123"
        }
        serializer = RegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_missing_password(self):
        """ Test for missing password """
        data = {
            "email": "testuser@example.com",
            "repeated_password": "password123"
        }
        serializer = RegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_missing_repeated_password(self):
        """ Test for missing repeated password """
        data = {
            "email": "testuser@example.com",
            "password": "password123",
        }
        serializer = RegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('repeated_password', serializer.errors)

    def test_short_password(self):
        """ Test for short password """
        data = {
            "email": "testuser@example.com",
            "password": "short",
            "repeated_password": "short"
        }
        serializer = RegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)
