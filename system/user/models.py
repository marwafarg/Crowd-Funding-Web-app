from django.db import models


from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

from PIL import Image
from django_countries.fields import CountryField
class User(AbstractUser):
    first_name = models.CharField(max_length=50,null=False)
    last_name = models.CharField(max_length=50,null=False)
    users = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True,related_name='profile')

    email_confirmed = models.BooleanField(default=False,null=True)
    phone_validation = RegexValidator(regex=r'^01[5|1|2|0][0-9]{8}$',
                                 message=" Please ,, Entered the Phone number in the format: '010|212|134|156'.")
    mobile_phone = models.CharField(max_length=11, null=True, blank=True , verbose_name=("Phone"))
    facebook =  models.URLField(null=True, blank=True , verbose_name=("FaceBook"))
    country = CountryField(null=True)
    birth_date = models.DateField(null=True, blank=True, verbose_name=("BirthDate"))
    profile_photo = models.ImageField(default='profile_pic/1.png',upload_to='profile_pic')



# Create your models here.
