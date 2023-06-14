
from django.http import HttpResponse
# from .Mixins import *
from Mufo.Minxins import *
from .serializers import *
from .models import Jockey_club_owner 
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status, response
from django.contrib.auth import authenticate,logout,login
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

from Audio_Jockey.models import Audio_Jockey
from Coins_club_owner.models import Coins_club_owner
from Coins_trader.models import Coins_trader
from User.models import User
import random


def Jockey_club_owners(request):
    return HttpResponse("Hello, world. You're at the Jockey_club_owner index.")


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


            email_exists = User.objects.filter(email=email).exists()
            phone_number_exists = User.objects.filter(phone=phone).exists()

            if email_exists or phone_number_exists:
                message = 'Email already exists as an User ' if email_exists else 'Phone number already exists as an User '
                return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            user = Jockey_club_owner.objects.get(email=serializer.data['email'])
            refresh = RefreshToken.for_user(user)
            messages.add_message(request, messages.INFO, f"New Audio jockey {user} is registered. please Approve ")
            return Response({'message': "Register successfully. Please wait for some time to Get Approved."}, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AudioJockeyList(APIView):
    def get(self, request, jockey_owner_id):
        try:
            audio_jockeys = Audio_Jockey.objects.filter(Club_Owner_Id=jockey_owner_id)
            audio_jockey_data = []
            for audio_jockey in audio_jockeys:
                audio_jockey_data.append({
                    'id': audio_jockey.id,
                    'name': audio_jockey.Name,
                    'email': audio_jockey.email,
                    # Add other fields you want to include
                })
            return Response(audio_jockey_data, status=status.HTTP_200_OK)
        except Jockey_club_owner.DoesNotExist:
            return Response({'message': 'Jockey Club Owner not found'}, status=status.HTTP_404_NOT_FOUND)

