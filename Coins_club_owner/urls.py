from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path("", views.coins_club_owner, name="index"),
    path("Register/", Register.as_view(), name="Register"),
    path("getallcointrader/<coin_club_owner_id>/", CointraderList.as_view(), name="getallcointrader"),
]
