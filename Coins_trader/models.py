from django.db import models

# Create your models here.
from django.db import models
import uuid
# Create your models here.
from Coins_club_owner.models import *

class Coins_trader(models.Model):
    Name = models.CharField(max_length=20, blank=False, null=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    Gender = models.CharField(max_length=20, default='')
    Dob = models.DateField(blank=True,  default='')
    profile_picture = models.CharField(max_length=200, default='', blank=True, null=True)
    Introduction_voice = models.CharField(max_length=200, default='', blank=True, null=True)
    Introduction_text = models.CharField(max_length=500, default='')
    Coins_Club_Owner_Id = models.ForeignKey(Coins_club_owner,on_delete=models.CASCADE)
    Coins_Club_Owner_Phone_Number = models.CharField(max_length=15)
    Coins_Clubs_Owner_Email_id = models.EmailField(max_length=254)
    National_ID = models.CharField(max_length=50,default='',null=True, blank=True)
    Pan_Card =models.CharField(max_length=50,default='',null=True, blank=True)
    Bank_Acc_Details = models.CharField(max_length=50,default='',null=True, blank=True)
    UPI_Address = models.CharField(max_length=50,default='',null=True, blank=True)
    Paytm_Address = models.CharField(max_length=50,default='',null=True, blank=True)
    otp = models.CharField(max_length=8, null=True, blank=True)
    uid = models.UUIDField(default=uuid.uuid4)
    forget_password_token = models.CharField(max_length=100, null=True, blank=True)
    Otpcreated_at = models.DateTimeField(null=True, blank=True)
    Is_Approved= models.BooleanField(default=False)


    def __str__(self):
        return self.Name

    @property
    def imageURL(self):
        try:
            url = self.profile_picture.url
        except:
            url = ''
        return url

    @property
    def documentURL(self):
        try:
            url = self.Introduction_voice.url
        except:
            url = ''
        return url
