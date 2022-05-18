from django.contrib.auth import authenticate
from authentication.models import User
import os
import random
from rest_framework.exceptions import AuthenticationFailed


def generate_username(name):
    username = "".join(name.split(" ")).lower()
    if not User.objects.filter(username=username).exists():
        return username
    else:
        random_username = f"{username}{random.randint(0,1000)}"
        return generate_username(random_username)


def register_social_user(provider, user_id, email, name):
    filtered_user_by_email = User.objects.filter(email=email)

    if filtered_user_by_email.exists():

        if provider == filtered_user_by_email[0].auth_provider:
            registered_user = authenticate(email=email, password=os.environ.get("SOCIAL_SECRET"))
        
            return {
                "username" : registered_user.username,
                "email" : registered_user.email,
                "tokens" : registered_user.tokens
            }
    
        else:
            raise AuthenticationFailed(f"Please continue your login using {filtered_user_by_email[0].auth_provider}")
    
    else:
        user_details = {
            "username" : generate_username(name),
            "email" : email,
            "provider" : provider
        }
        _user = User.objects.create(**user_details)
        _user.is_active = True
        _user.auth_provider = provider
        _user.save()

        user = authenticate(email=_user.email, password=os.environ.get("SOCIAL_SECRET"))
        return {
            "username" : user.username,
            "email" : user.email,
            "tokens" : user.tokens
        }
