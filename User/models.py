from django.db import models
import uuid
# Create your models here.


class User(models.Model):
    Name = models.CharField(max_length=20, blank=False, null=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    Gender = models.CharField(max_length=20, default='')
    Dob = models.DateField(blank=True,  default='')
    profile_picture = models.CharField(max_length=200, default='', blank=True, null=True)
    Introduction_voice = models.CharField(max_length=200, default='', blank=True, null=True)
    Introduction_text = models.CharField(max_length=500, default='')
    Invitation_Code = models.IntegerField(null=True, blank=True)
    otp = models.CharField(max_length=8, null=True, blank=True)
    uid = models.UUIDField(default=uuid.uuid4)
    forget_password_token = models.CharField(max_length=100, null=True, blank=True)
    Otpcreated_at = models.DateTimeField(null=True, blank=True)

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
