from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views
from .views import *

urlpatterns = [
    path("", views.Users, name="User"),
    path("Register/", Register.as_view(), name="Register"),
    path('login/', Login.as_view(), name="login"),
    path('otp/<uid>/', Otp.as_view() , name='otp'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
