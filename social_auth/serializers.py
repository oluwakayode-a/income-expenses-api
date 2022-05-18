import imp
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from social_auth.register import register_social_user
from .google import Google
from .facebook import Facebook
import os

class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError("Token invalid. Please login again.")
        

        if user_data["aud"] != os.environ.get("GOOGLE_CLIENT_ID"):
            raise AuthenticationFailed("Unauthorized request.", 401)
        
        user_id = user_data["sub"]
        email = user_data["email"]
        name = user_data["name"]
        provider = "google"

        return register_social_user(user_id=user_id, email=email, name=name, provider=provider)


class FacebookSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = Facebook.validate(auth_token)
        try:
            user_id = user_data["id"]
            email = user_data["email"]
            name = user_data["name"]
            provider = "facebook"

            return register_social_user(user_id=user_id, email=email, name=name, provider=provider)
        except Exception as e:
            raise serializers.ValidationError("Token invalid. Please login again.")