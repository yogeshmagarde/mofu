from django.http import HttpResponse
from Mufo.Minxins import *
from .serializers import *

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status, response
from django.contrib.auth import authenticate,logout,login
import random
from django.utils import timezone
from datetime import timedelta

from django.utils import timezone
from datetime import timedelta

from .models import User 
from Audio_Jockey.models import Audio_Jockey
from Coins_club_owner.models import Coins_club_owner
from Coins_trader.models import Coins_trader
from Jockey_club_owner.models import Jockey_club_owner


def Users(request):
    return HttpResponse("Hello, world. You're at the User index.")


class Register(APIView):
    serializer_class = UserSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        phone=serializer.initial_data.get('phone')
        email=serializer.initial_data.get('email')
        if serializer.is_valid():

            email_exists = Audio_Jockey.objects.filter(email=email).exists()
            phone_number_exists = Audio_Jockey.objects.filter(phone=phone).exists()

            if email_exists or phone_number_exists:
                message = 'Email already exists as an Audio_Jockey ' if email_exists else 'Phone number already exists as an Audio_Jockey '
                return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

            email_exists = Coins_club_owner.objects.filter(email=email).exists()
            phone_number_exists = Coins_club_owner.objects.filter(phone=phone).exists()

            if email_exists or phone_number_exists:
                message = 'Email already exists as coin club owner ' if email_exists else 'Phone number already exists as coin club owner'
                return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
            
            email_exists = Coins_trader.objects.filter(email=email).exists()
            phone_number_exists = Coins_trader.objects.filter(phone=phone).exists()

            if email_exists or phone_number_exists:
                message = 'Email already exists as an Coins_trader ' if email_exists else 'Phone number already exists as an Coins_trader '
                return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)


            email_exists = Jockey_club_owner.objects.filter(email=email).exists()
            phone_number_exists = Jockey_club_owner.objects.filter(phone=phone).exists()

            if email_exists or phone_number_exists:
                message = 'Email already exists as an Jockey_club_owner ' if email_exists else 'Phone number already exists as an Jockey_club_owner '
                return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)


            serializer.save()
            user = User.objects.get(email=serializer.data['email'])
            refresh = RefreshToken.for_user(user)
            return Response({'data': str(serializer.data), 'refresh': str(refresh), 'access': str(refresh.access_token), 'message': "Register successfully"}, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class Login(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        phone = serializer.initial_data.get('phone')

        # Check if the phone number exists in any of the profile models
        profiles = [Audio_Jockey, Coins_club_owner, Coins_trader, Jockey_club_owner,User]
        profile = None

        for profile_model in profiles:
            profile = profile_model.objects.filter(phone=phone).first()
            if profile:
                break

        if not profile:
            return Response({'message': "No user found with this mobile"}, status=status.HTTP_404_NOT_FOUND)

        if not profile.Is_Approved:
            return Response({'message': f"{profile.__class__.__name__} {profile} is not approved Yet. Please wait for some time to get approved."}, status=status.HTTP_403_FORBIDDEN)

        user = profile.__class__.objects.get(phone=phone)
        current_time = timezone.now()
        if user.Otpcreated_at and user.Otpcreated_at > current_time:
            user.otp = random.randint(1000, 9999)
            user.Otpcreated_at = current_time + timedelta(minutes=5)
        else:
            user.otp = random.randint(1000, 9999)
            user.Otpcreated_at = current_time + timedelta(minutes=5)

        user.save()
        # send_otp_on_phone(phone, user.otp)
        return Response({'uid': str(user.uid), 'otp': str(user.otp), 'message': "Otp sent successfully"})


class Otp(APIView):
    serializer_class = OtpSerializer

    def post(self, request, uid):
        serializer = self.serializer_class(data=request.data)
        otp = serializer.initial_data.get('otp')
        profiles = [Audio_Jockey, Jockey_club_owner, Coins_trader, Coins_club_owner,User]
        profile = None

        for profile_model in profiles:
            profile = profile_model.objects.filter(uid=uid).first()
            if profile:

                break

        current_time = timezone.now()
        if otp == profile.otp and profile.Otpcreated_at and profile.Otpcreated_at > current_time:
            refresh = RefreshToken.for_user(profile)
            user_serializer = UserSerializer(profile)
            return Response({'data': str(user_serializer.data),'profile':str(profile.__class__.__name__) ,'id': str(profile.id), 'refresh': str(refresh), 'access': str(refresh.access_token), 'message': "Login successfully"})
        else:
            return Response({'message': "Invalid OTP. Please try again"}, status=status.HTTP_400_BAD_REQUEST)
