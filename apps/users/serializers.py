from faker import Faker

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

User = get_user_model()


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    def validate_username(self, username):

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username already in use")
        return username

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Password do not match")

        validate_password(data["password"])
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)

        fake = Faker()
        email = fake.ascii_email()
        while User.objects.filter(email=email).exists():
            email = fake.ascii_email()
        validated_data["email"] = email

        user = User.objects.create_user(**validated_data, is_active=True)
        return user


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            raise serializers.ValidationError({"bad_token": _("Token is invalid or expired")})
