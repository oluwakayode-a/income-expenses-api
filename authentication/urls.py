from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginView, PasswordTokenCheckView, RegisterView, RequestPasswordResetEmail, SetNewPasswordView, VerifyEmail

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("email-verify/", VerifyEmail.as_view(), name='verify_email'),
    path("token/refresh", TokenRefreshView.as_view(), name="token-refresh"),
    path("login/", LoginView.as_view(), name="login"),
    path("request-reset-email/", RequestPasswordResetEmail.as_view(), name="request-reset-email"),
    path("password-reset/<uidb64>/<token>/", PasswordTokenCheckView.as_view(), name='password-reset-confirm'),
    path("password-reset-complete/", SetNewPasswordView.as_view(), name="password-reset-complete"),
]