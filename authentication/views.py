from django.shortcuts import redirect
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from authentication.renderers import UserRenderer
from incomeexpensesapi.settings import SECRET_KEY
from .serializers import RegisterSerializer, LoginSerializer, LogoutSerializer, RequestEmailSerializer, SetNewPasswordSerializer
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


# Create your views here.
class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        _user = User.objects.get(email=user_data["email"])

        token = RefreshToken.for_user(user=_user).access_token
        
        url = f"http://{get_current_site(request).domain}{reverse('verify_email')}?token={token}"
        data = {
            "body" : f"Hi, {_user.username}, use the link below to verify your email. \n {url}",
            "subject" : "Verify Email",
            "email" : _user.email
        }
        Util.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(APIView):
    renderer_classes = (UserRenderer,)

    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description="Input token", type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get("token")
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])

            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({"email" : "Successfully activated."}, status=status.HTTP_200_OK)
        except jwt.exceptions.ExpiredSignatureError:
            return Response({"error" : "Activation link expired."}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({"error" : "Token Invalid"}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    renderer_classes = (UserRenderer,)


    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestPasswordResetEmail(GenericAPIView):
    serializer_class = RequestEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(email=serializer.data['email'])
        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))

        token = PasswordResetTokenGenerator().make_token(user)
        redirect_url = request.data.get('redirect_url', '')

        url = f"http://{get_current_site(request).domain}{reverse('password-reset-confirm', kwargs={'uidb64':uidb64, 'token' : token})}?redirect_url={redirect_url}"
        data = {
            "body": f"Hi, {user.username}, use the link below to reset your password. \n {url}",
            "subject": "Reset Password",
            "email": user.email
        }
        Util.send_email(data)

        return Response({"success" : "We have sent you a link to reset your password."}, status=status.HTTP_200_OK)


class PasswordTokenCheckView(APIView):
    def get(self, request, uidb64, token):
        redirect_url = request.GET.get('redirect_url', '')

        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            
            if not PasswordResetTokenGenerator().check_token(user, token):
                if redirect_url:
                    return redirect(f"{redirect_url}?token_valid=False")
                # return Response({"error" : "Invalid Token"}, status=status.HTTP_401_UNAUTHORIZED)
        except UnicodeDecodeError:
            # return Response({"error" : "Token Error"}, status=status.HTTP_400_BAD_REQUEST)
            return redirect(f"{redirect_url}?token_valid=False")
        
        # return Response({"success" : True}, status=status.HTTP_200_OK)
        return redirect(f"{redirect_url}?token_valid=True&?token={token}&?uidb64={uidb64}")


class SetNewPasswordView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({"success" : True, "message" : "Password Reset Successful."}, status=status.HTTP_200_OK)


class LogOutView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)