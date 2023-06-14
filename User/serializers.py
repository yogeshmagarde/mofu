from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model =User
        fields =('phone',)

class OtpSerializer(serializers.ModelSerializer):
    class Meta:
        model =User
        fields =('otp',)