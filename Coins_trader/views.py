
from django.http import HttpResponse
# from .Mixins import *
from Mufo.Minxins import *
from .serializers import *
from .models import Coins_trader
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status, response
from django.contrib.auth import authenticate,logout,login
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
import random

from Audio_Jockey.models import Audio_Jockey
from Coins_club_owner.models import Coins_club_owner
from User.models import User
from Jockey_club_owner.models import Jockey_club_owner

def coins_trader(request):
    return HttpResponse("Hello, world. You're at the Coins_trader index.")


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
            
            email_exists = User.objects.filter(email=email).exists()
            phone_number_exists = User.objects.filter(phone=phone).exists()

            if email_exists or phone_number_exists:
                message = 'Email already exists as an User ' if email_exists else 'Phone number already exists as an User '
                return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)


            email_exists = Jockey_club_owner.objects.filter(email=email).exists()
            phone_number_exists = Jockey_club_owner.objects.filter(phone=phone).exists()

            if email_exists or phone_number_exists:
                message = 'Email already exists as an Jockey_club_owner ' if email_exists else 'Phone number already exists as an Jockey_club_owner '
                return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            user = Coins_trader.objects.get(email=serializer.data['email'])
            refresh = RefreshToken.for_user(user)
            messages.add_message(request, messages.INFO, f"New Coins Trader {user} is registered. please Approve ")
            return Response({'message': "Register successfully. Please wait for some time to Get Approved."}, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CointraderConnectedOwner(APIView):
    def get(self, request, coin_trader_id):
        try:
            coin_trader = Coins_trader.objects.get(id=coin_trader_id)
            print(coin_trader)
            connected_owner = coin_trader.Coins_Club_Owner_Id
            if connected_owner:
                owner_data = {
                    'id': connected_owner.id,
                    'name': connected_owner.Name,
                    'email': connected_owner.email,
                }
                return Response(owner_data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No connected Jockey Club Owner found'}, status=status.HTTP_404_NOT_FOUND)
        except Coins_trader.DoesNotExist:
            return Response({'message': 'coin trader not found'}, status=status.HTTP_404_NOT_FOUND)

