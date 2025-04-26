from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import admin
#from .models import User

# Register your models here.
#admin.site.register(User)

# Create your models here.
class User(AbstractUser):
    pass