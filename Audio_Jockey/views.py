
from django.http import HttpResponse
# from .Mixins import *
from Mufo.Minxins import *
from .serializers import *
from .models import Audio_Jockey
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status, response
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages

from django.utils import timezone
from datetime import timedelta

from User.models import User
from Coins_club_owner.models import Coins_club_owner
from Coins_trader.models import Coins_trader
from Jockey_club_owner.models import Jockey_club_owner

import random


from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


def audio_jockey(request):
    return HttpResponse("Hello, world. You're at the Audio_jockey index.")


class Register(APIView):
    serializer_class = UserSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        phone = serializer.initial_data.get('phone')
        email = serializer.initial_data.get('email')
        if serializer.is_valid():

            email_exists = User.objects.filter(email=email).exists()
            phone_number_exists = User.objects.filter(phone=phone).exists()

            if email_exists or phone_number_exists:
                message = 'Email already exists as an users ' if email_exists else 'Phone number already exists as an users '
                return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

            email_exists = Coins_club_owner.objects.filter(
                email=email).exists()
            phone_number_exists = Coins_club_owner.objects.filter(
                phone=phone).exists()

            if email_exists or phone_number_exists:
                message = 'Email already exists as coin club owner ' if email_exists else 'Phone number already exists as coin club owner'
                return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

            email_exists = Coins_trader.objects.filter(email=email).exists()
            phone_number_exists = Coins_trader.objects.filter(
                phone=phone).exists()

            if email_exists or phone_number_exists:
                message = 'Email already exists as an Coins_trader ' if email_exists else 'Phone number already exists as an Coins_trader '
                return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

            email_exists = Jockey_club_owner.objects.filter(
                email=email).exists()
            phone_number_exists = Jockey_club_owner.objects.filter(
                phone=phone).exists()

            if email_exists or phone_number_exists:
                message = 'Email already exists as an Jockey_club_owner ' if email_exists else 'Phone number already exists as an Jockey_club_owner '
                return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            user = Audio_Jockey.objects.get(email=serializer.data['email'])
            refresh = RefreshToken.for_user(user)
            messages.add_message(
                request, messages.INFO, f"New Audio jockey {user} is registered. please Approve ")
            return Response({'message': "Register successfully. Please wait for some time to Get Approved."}, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AudioJockeyConnectedOwner(APIView):
    def get(self, request, audio_jockey_id):
        try:
            audio_jockey = Audio_Jockey.objects.get(id=audio_jockey_id)
            connected_owner = audio_jockey.Club_Owner_Id
            if connected_owner:
                owner_data = {
                    'id': connected_owner.id,
                    'name': connected_owner.Name,
                    'email': connected_owner.email,
                }
                return Response(owner_data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No connected Jockey Club Owner found'}, status=status.HTTP_404_NOT_FOUND)
        except Audio_Jockey.DoesNotExist:
            return Response({'message': 'Audio Jockey not found'}, status=status.HTTP_404_NOT_FOUND)

