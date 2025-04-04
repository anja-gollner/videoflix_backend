from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True, required=True, min_length=6)
    repeated_password = serializers.CharField(
        write_only=True, required=True, min_length=6)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Diese E-Mail-Adresse wird bereits verwendet.")
        return value

    def validate(self, data):
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError(
                {"repeated_password": "Die Passwörter stimmen nicht überein."})
        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            raise serializers.ValidationError(
                {"detail": ["Benutzername und Passwort sind erforderlich."]})
        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                raise serializers.ValidationError(
                    {"detail": ["Bitte bestätige zuerst deine E-Mail-Adresse."]}
                )
            user = authenticate(username=user.username, password=password)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"detail": ["Ungültige Anmeldeinformationen."]})
        if user is None:
            raise serializers.ValidationError(
                {"detail": ["Ungültige Anmeldeinformationen."]})
        token, created = Token.objects.get_or_create(user=user)
        return {
            "token": token.key,  
            "user_id": user.id,
            "email": user.email
        }

