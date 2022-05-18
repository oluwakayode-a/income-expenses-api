from django.urls import path
from .views import FacebookSocialAuthView, GoogleSocialAuthView

urlpatterns = [
    path("google/", GoogleSocialAuthView.as_view(), name='google'),
    path("facebook/", FacebookSocialAuthView.as_view(), name="facebook")
]