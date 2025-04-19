from django.db import models
import uuid ,random

class nidUser(models.Model):
    Fname = models.CharField(max_length=100)
    Lname = models.CharField(max_length=100)
    sex = models.CharField(max_length=100)
    FAN = models.CharField(max_length=12,unique=True)
    phone_number = models.IntegerField()
    
# Create your models here.