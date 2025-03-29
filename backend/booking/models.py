from django.db import models
from user.models import user, branch
from vehicle_management.models import vehicle

import sys
sys.path.append("..")

class route(models.Model):

    name = models.CharField(max_length=50)
    first_destination = models.CharField(max_length=50)
    last_destination = models.CharField(max_length=50)
    prize = models.DecimalField(max_digits=10 , decimal_places=2)



class ticket(models.Model):
    time = models.TimeField()
    date = models.DateField()
    bought_date = models.DateTimeField(auto_now_add=True)
    route = models.ForeignKey(route,on_delete=models.DO_NOTHING , related_name='route')
    vehicle = models.ForeignKey(vehicle, on_delete=models.DO_NOTHING,related_name='vehicle')
    user = models.ForeignKey(user,on_delete=models.CASCADE , related_name='user')
    additional = models.DecimalField(max_digits=10 , decimal_places=2 , default=1)
    branch = models.ForeignKey(branch, on_delete=models.SET_NULL,null=True , related_name='branch')

