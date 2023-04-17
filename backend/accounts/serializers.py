from rest_framework import serializers
from rest_framework.settings import api_settings
from rest_framework.exceptions import AuthenticationFailed

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.models import update_last_login

from accounts.models import Profile
from accounts.email import create_email
from accounts.tokens import decode_token


User = get_user_model()


class LoginSeralizer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)
    email = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)
    access_token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['username','password','email','refresh_token','access_token']
    

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError({"error":"Invalid Creditials"})
        if not user.is_active:
            raise serializers.ValidationError({"error":"Sorry! cannot login deactivte account."})
        tokens = user.get_tokens()
        update_last_login(None, user=user)
        return {
            'email':user.email,
            'username':user.username,
            'refresh_token':tokens['refresh'],
            'access_token':tokens['access'],
        }
    
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token  = attrs['refresh']
        return attrs
    
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail("Bad Token")

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)
    confirm_password = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ['username','email','password','confirm_password']

    
    def validate(self, attrs):
        username = attrs.get("username")
        email = attrs.get("email")
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")
        if len(username) < 4:
            raise serializers.ValidationError({"error":"username must be of length more than 4"})
        if not username.isalnum():
            raise serializers.ValidationError({"error":"username must be combination of letters and number or letters only"})
        if password != confirm_password:
            raise serializers.ValidationError({"error":"password and confirm password does not match"})
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"error":"username already exists"})
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error":"email already exists"})
        user = User(username=username, email=email)
        try:
            validate_password(password=password, user=user)
        except ValidationError as e:
            serializers_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError({
                "password": serializers_error[api_settings.NON_FIELD_ERRORS_KEY]
            })
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class EmailVerifySerializer(serializers.ModelSerializer):
    token =serializers.CharField()
    class Meta:
        model = User
        fields = ["token"]


class ResendEmailConfirmationLinkSerailzer(serializers.ModelSerializer):
    email_confirmed = serializers.BooleanField(read_only=True)
    class Meta:
        model = User
        fields = ['email_confirmed']
        

class SimpleUserSerializer(serializers.ModelSerializer):
    email_confirmed = serializers.BooleanField(read_only=True)
    class Meta:
        model = User
        fields = ['username','email','email_confirmed']
        


class UserDetailSerailizer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)
    email_confirmed = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','email_confirmed','is_active','date_joined','last_login']


class ProfileSeralizer(serializers.ModelSerializer):
    user = UserDetailSerailizer()

    class Meta:
        model = Profile
        fields = ['user','avatar','bio','gender','facebook','twitter','github']

class ProfileEditSerializer(serializers.ModelSerializer):
    user = UserDetailSerailizer()
    class Meta:
        model = Profile
        fields = ['user','avatar','bio','gender','facebook','twitter','github']


    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        user = User.objects.get(profile=instance)
        user.first_name = user_data.get("first_name", user.first_name)
        user.last_name = user_data.get("last_name", user.last_name)
        user.save()
        instance.save()
        return instance



class PasswordChangeSerilaizer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['old_password','password','password_confirm']
    
    def validate(self, attrs):
        old_password = attrs.get("old_password")
        password = attrs.get("password")
        password_confirm = attrs.get("password_confirm")
        user = self.context['user'] or None
        if user is not None:
            if not user.check_password(old_password):
                raise AuthenticationFailed({"error":"old password does not mathch"})
            if password != password_confirm:
                raise AuthenticationFailed({"error":"confirm password does not match"})
            user.set_password(password)
            user.save()
            return user
        return super().validate(attrs)


class PasswordResetLinkSerializer(serializers.Serializer):
    email = serializers.EmailField()
    class Meta:
        fields = ["email",]
    
    def validate(self, attrs):
        email = attrs.get("email")
        try:
            if not User.objects.filter(email=email).exists():
                raise serializers.ValidationError({"error":f"user with {email} does not exist"})
        except User.DoesNotExist:
            raise serializers.ValidationError({"error":"user does not exist"})
        user = User.objects.get(email=email)
        create_email(username=user.username, email=email, action="password_reset", current_site=self.context['current_site'])
        return attrs


class PasswordResetSerializer(serializers.ModelSerializer):
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    new_password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["token", "new_password","new_password_confirm"]
    
    def validate(self, attrs):
        password1 = attrs.get("new_password", '')
        password2 = attrs.get("new_password_confirm", '')
        token = attrs.get("token")
        username, verify_status = decode_token(token)
        user = User.objects.get(username=username)
        try:
            validate_password(password=password1, user=user)
        except ValidationError as e:
            serializers_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError({
                "password": serializers_error[api_settings.NON_FIELD_ERRORS_KEY]
            })      
        if password1 != password2:
            raise serializers.ValidationError({"error":"password mismatch"})
        user.set_password(password1)
        user.save()
        return attrs
    
    
class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email']