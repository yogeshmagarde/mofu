
from django.http import HttpResponse
# from .Mixins import *
from Mufo.Minxins import *
from .serializers import *
from .models import Coins_club_owner 
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
from User.models import User
from Coins_trader.models import Coins_trader
from Jockey_club_owner.models import Jockey_club_owner

import random
def coins_club_owner(request):
    return HttpResponse("Hello, world. You're at the Coins_club_owner index.")

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

            email_exists = User.objects.filter(email=email).exists()
            phone_number_exists = User.objects.filter(phone=phone).exists()

            if email_exists or phone_number_exists:
                message = 'Email already exists as User ' if email_exists else 'Phone number already exists as User'
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
            user = Coins_club_owner.objects.get(email=serializer.data['email'])
            refresh = RefreshToken.for_user(user)
            messages.add_message(request, messages.INFO, f"New coins club owner {user} is registered. please Approve ")
            return Response({'message': "Register successfully. Please wait for some time to Get Approved."}, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CointraderList(APIView):
    def get(self, request, coin_club_owner_id):
        try:
            coin_traders = Coins_trader.objects.filter(Coins_Club_Owner_Id=coin_club_owner_id)
            coin_trader_data = []
            for coin_trader in coin_traders:
                coin_trader_data.append({
                    'id': coin_trader.id,
                    'name': coin_trader.Name,
                    'email': coin_trader.email,
                    'image':coin_trader.imageURL
                    # Add other fields you want to include
                })
            return Response(coin_trader_data, status=status.HTTP_200_OK)
        except Jockey_club_owner.DoesNotExist:
            return Response({'message': 'Coin Club Owner not found'}, status=status.HTTP_404_NOT_FOUND)


