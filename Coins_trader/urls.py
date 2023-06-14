from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path("", views.coins_trader, name="coins_trader"),
    path("Register/", Register.as_view(), name="Register"),
    path("getcoin_club_owner/<coin_trader_id>/", CointraderConnectedOwner.as_view(), name="getcoin_club_owner"),
]
