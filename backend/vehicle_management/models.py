from django.db import models
from user.models import user,branch


import sys
sys.path.append("..")
class vehicle(models.Model):
    branch = models.ForeignKey(branch, on_delete=models.SET_NULL, null = True)
    name = models.CharField(max_length=100)
    plate_number = models.IntegerField(unique= True)
    color = models.CharField(max_length=50)
    Model = models.CharField(max_length=100)
    sit_number = models.IntegerField(default=0)
    picture = models.ImageField(upload_to='vehicle_management/vehicle_image')
    user = models.ForeignKey(user,on_delete=models.SET_NULL , null=True)

class type(models.Model):
    class level_type(models.TextChoices):
        LEVEL_ONE = 'lo',('level_one')
        LEVEL_TWO = 'lt',('level_two')
        LEVEL_THREE = 'lth',('level_three')
    
    level = models.CharField(max_length=12, choices=level_type.choices,default=level_type.LEVEL_ONE)
    detail = models.TextField()
    prize = models.DecimalField(max_digits=10 , decimal_places=2)

   
class documentation (models.Model):
    doc = models.FileField(upload_to='vehicle_management/doc')
    did = models.CharField(max_length=100, unique=True)
    vehicle = models.ForeignKey(vehicle , on_delete=models.CASCADE,related_name='vehicle_doc')



