from rest_framework import serializers
from .models import User,Follow


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


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('Name','email','Gender','Dob','profile_picture','Introduction_voice','Introduction_text')


class FollowerSerializer(serializers.ModelSerializer):
    user = UserUpdateSerializer()

    class Meta:
        model = Follow
        fields = ('user', 'created_at')


class FollowingSerializer(serializers.ModelSerializer):
    following_user = UserUpdateSerializer()

    class Meta:
        model = Follow
        fields = ('following_user', 'created_at')
