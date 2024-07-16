from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from integrations.notifications.email_notification import EmailNotification


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','first_name','email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            email=validated_data['email']
        )
        EmailNotification.send_welcome_email.delay(
            {
                "email": validated_data['email'],
                "first_name": validated_data['first_name']
            }
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = User.objects.filter(email=data['email']).last()
        if user and user.check_password(data['password']):
            return user
        raise serializers.ValidationError(
            "Invalid credentials"
        )