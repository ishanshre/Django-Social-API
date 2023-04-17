from django.shortcuts import render, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model

from accounts.email import create_email
from accounts.models import Profile
from accounts.tokens import decode_token
from accounts.serializers import (
    LoginSeralizer,
    LogoutSerializer,
    RegisterSerializer,
    EmailVerifySerializer,
    ResendEmailConfirmationLinkSerailzer,
    SimpleUserSerializer,
    ProfileSeralizer,
    ProfileEditSerializer,
    PasswordChangeSerilaizer,
    PasswordResetLinkSerializer,
    PasswordResetSerializer,
)

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
# Create your views here.

User = get_user_model()
class LoginApiView(GenericAPIView):
    serializer_class = LoginSeralizer


    def post(self, request, *args, **kwargs):
        serailizer = self.serializer_class(data=request.data)
        serailizer.is_valid(raise_exception=True)

        return Response(serailizer.data, status=status.HTTP_200_OK)
        
class LogoutApiView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success":"logout successfull"}, status=status.HTTP_200_OK)

class RegisterApiView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        current_site = get_current_site(request=request).domain
        create_email(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
            action="email_verify",
            current_site=current_site
        )
        return Response(
            {
                "done": serializer.data,
                "message":"please check your email to verify your email address",
            }, status=status.HTTP_201_CREATED
        )


class VerifyEmail(GenericAPIView):
    serializer_class = EmailVerifySerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.data['token']
        username, verify_status = decode_token(token)
        if verify_status:
            user = get_object_or_404(User, username=username)
            user.email_confirmed = True
            user.save()
            return Response({
                "done":"email verified"}, status=status.HTTP_200_OK
            )
        return Response({
            "error":"invalid token"
        }, status=status.HTTP_400_BAD_REQUEST)



class ResendEmailLinkApiView(GenericAPIView):
    serializer_class = ResendEmailConfirmationLinkSerailzer
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(instance=request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        current_site = get_current_site(request=request).domain
        if not request.user.email_confirmed:
            create_email(
                username=request.user.username,
                email=request.user.email,
                action="email_verify",
                current_site=current_site
            )
            return Response({"done":"email confirm link sent to your mail"}, status=status.HTTP_200_OK)
        return Response({"error":"email already confirmed"})



class UserApiView(GenericAPIView):
    serializer_class = SimpleUserSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return self.request.user
    def get(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.serializer_class(instance=instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        instance = request.user
        serializer =self.serializer_class(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        username = serializer.validated_data['username']
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileDetailUpdateApiView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get','put']
    
    def get_queryset(self):
        return Profile.objects.get(user=self.request.user)

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "PUT":
            return ProfileEditSerializer
        return ProfileSeralizer
    
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        profile = self.get_queryset()
        serializer = serializer(instance=profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        profile = self.get_queryset()
        serializer = serializer(instance=profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordChangeApiView(GenericAPIView):
    serializer_class = PasswordChangeSerilaizer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.context['user'] = request.user
        serializer.is_valid(raise_exception=True)
        return Response({
            "Success": "Password Change Success Full"
        }, status=status.HTTP_200_OK)


class PasswordResetLinkApiView(GenericAPIView):
    serializer_class = PasswordResetLinkSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        current_site = get_current_site(request=request).domain
        serializer.context['current_site']=current_site
        serializer.is_valid(raise_exception=True)
        return Response({"success":f"Password Reset Link has been sent to your email {serializer.validated_data['email']}."})


class PasswordResetApiView(GenericAPIView):
    serializer_class = PasswordResetSerializer
    http_method_names = ['post']
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"success":"Your Password Changed Successfull"})
     
        
