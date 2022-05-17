from django.forms import ValidationError
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.contrib import auth
from authentication.models import User
from django.contrib.sites.shortcuts import get_current_site
from .utils import Util
from django.urls import reverse
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68,
                                     min_length=5,
                                     write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                "Username cannot contain special characters.")
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = [
            "token",
        ]


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=5)
    password = serializers.CharField(max_length=68,
                                     min_length=5,
                                     write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "tokens"]

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed("Invalid email or password.")

        if not user.is_active:
            raise AuthenticationFailed(
                "Your account has been deactivated. Please contact admin.")

        if not user.is_verified:
            raise AuthenticationFailed("Email is not verified.")

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }


class RequestEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = [
            "email",
        ]

    def validate(self, attrs):
        email = attrs.get('email', '')
        if not User.objects.filter(email=email).exists():
            raise ValidationErr("User does not exist.")
        return super().validate(attrs)


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=80, write_only=True)
    token = serializers.CharField(min_length=1, max_length=500)
    uidb64 = serializers.CharField(min_length=1, max_length=500)

    class Meta:
        fields = "__all__"
    

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError("Reset link invalid.")
            
            user.set_password(password)
            user.save()

            return user
        except Exception as e:
            raise serializers.ValidationError("Reset link invalid")