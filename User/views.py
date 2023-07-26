from django.http import HttpResponse,JsonResponse
from Mufo.Minxins import *
from .serializers import *

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status, response
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
import secrets
from django.utils.decorators import method_decorator
from Mufo.Minxins import authenticate_token
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
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

            token = secrets.token_hex(128)
            serializer.save(token =token)
            return Response({'data': str(serializer.data), 'access': str(token), 'message': "Register successfully"}, status=status.HTTP_201_CREATED)

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

        if hasattr(profile, 'Is_Approved') and not profile.Is_Approved:
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
        profiles = [Audio_Jockey, Coins_club_owner, Coins_trader, Jockey_club_owner,User]
        profile = None

        for profile_model in profiles:
            try:
                profile = profile_model.objects.get(uid=uid)
                break
            except profile_model.DoesNotExist:
                continue

        current_time = timezone.now()
        if otp == profile.otp and profile.Otpcreated_at and profile.Otpcreated_at > current_time:
            user_serializer = UserSerializer(profile)
            return Response({'data': (user_serializer.data),'profile':str(profile.__class__.__name__) ,'id': str(profile.id),  'access': str(profile.token), 'message': "Login successfully"})
        else:
            return Response({'message': "Invalid OTP. Please try again"}, status=status.HTTP_400_BAD_REQUEST)



class UpdateUser(APIView):
    @method_decorator(authenticate_token)
    def get(self, request, format=None):
        pk = request.user.id
        user = User.objects.get(id=pk)
        serializer = UserUpdateSerializer(user)
        return Response(serializer.data)
    @method_decorator(authenticate_token)
    def put(self, request,format=None):
        pk = request.user.id
        user = User.objects.get(id=pk)
        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    @method_decorator(authenticate_token)
    def delete(self, request, format=None):
        pk = request.user.id
        user = User.objects.get(id=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class Searchalluser(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [SearchFilter]
    search_fields = ['Name','email']



class FollowUser(APIView):
    @method_decorator(authenticate_token)
    def post(self, request, follow):
        try:
            following_user = User.objects.get(id=follow)
            follow_user, created = Follow.objects.get_or_create(user=request.user, following_user=following_user)
            
            if not created:
                follow_user.delete()
                return Response({'success': True, 'message': 'Unfollowed user.'})
            else:
                return Response({'success': True, 'message': 'Followed user.'})
        
        except User.DoesNotExist:
            return Response({'success': False, 'message': 'User does not exist.'})


class FollowerList(APIView):
    @method_decorator(authenticate_token)
    def get(self, request):
        followers = Follow.objects.filter(following_user_id=request.user.id)
        serializer = FollowerSerializer(followers, many=True)
        return Response(serializer.data)


class FollowingList(APIView):
    @method_decorator(authenticate_token)
    def get(self, request):
        following = Follow.objects.filter(user_id=request.user.id)
        serializer = FollowingSerializer(following, many=True)
        return Response(serializer.data)
    



@method_decorator(authenticate_token, name='dispatch')
class userview(APIView):
    def get(self, request):
        user = request.user
        print(user)
        return JsonResponse({'uid': user.uid, 'number': user.phone,"name":user.Name})

