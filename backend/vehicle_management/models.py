from django.db import models
from user.models import user,branch


import sys
sys.path.append("..")

class route(models.Model):

    name = models.CharField(max_length=50)
    first_destination = models.ForeignKey(branch, on_delete=models.CASCADE, related_name='origin',null=True)
    last_destination = models.ForeignKey(branch, on_delete=models.CASCADE, related_name='destination',null=True)
    route_prize = models.DecimalField(max_digits=10 , decimal_places=2)


class type(models.Model):
    class level_type(models.TextChoices):
        LEVEL_ONE = 'one',('level_one')
        LEVEL_TWO = 'two',('level_two')
        LEVEL_THREE = 'three',('level_three')
        OTHER = 'other',('other')
    
    level = models.CharField(max_length=12, choices=level_type.choices,default=level_type.LEVEL_ONE)
    detail = models.TextField()
    prize = models.DecimalField(max_digits=10 , decimal_places=2)

class location(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    timestamp = models.DateTimeField(auto_now_add=True)
    
class vehicle(models.Model):
    branch = models.ForeignKey(branch, on_delete=models.SET_NULL, null = True)
    name = models.CharField(max_length=100)
    plate_number = models.CharField(max_length=10 ,unique= True)
    color = models.CharField(max_length=50)
    year = models.CharField(max_length=10,null=True)
    Model = models.CharField(max_length=100)
    sit_number = models.IntegerField(default=0)
    picture = models.ImageField(upload_to='vehicle_management/vehicle_image')
    is_active =models.BooleanField(default=False)
    user = models.ForeignKey(user,on_delete=models.SET_NULL , null=True, related_name="driver")
    types = models.ForeignKey(type, on_delete=models.SET_NULL, null=True)
    location = models.ForeignKey(location , on_delete=models.SET_NULL , null=True)
    last_updated = models.DateTimeField(auto_now=True)
    route = models.ForeignKey(route ,on_delete=models.SET_NULL , null= True )
    insurance_doc = models.ImageField(upload_to='vehicle_management/insurance_doc',null=True)
    insurance_date = models.DateField(null=True)
class documentation (models.Model):
    doc = models.FileField(upload_to='vehicle_management/doc')
    did = models.CharField(max_length=100, unique=True)
    vehicle = models.ForeignKey(vehicle , on_delete=models.CASCADE,related_name='vehicle_doc')



