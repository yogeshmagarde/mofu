from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path("", views.audio_jockey, name="index"),
    path("Register/", Register.as_view(), name="Register"),
    path("getjockey_owner/<audio_jockey_id>/", AudioJockeyConnectedOwner.as_view(), name="getjockey_owner"),
]
