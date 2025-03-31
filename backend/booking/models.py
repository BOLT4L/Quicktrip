from django.db import models
from user.models import user, branch
from vehicle_management.models import vehicle, type

import sys
sys.path.append("..")

class route(models.Model):

    name = models.CharField(max_length=50)
    first_destination = models.ForeignKey(branch, on_delete=models.CASCADE, related_name='origin',null=True)
    last_destination = models.ForeignKey(branch, on_delete=models.CASCADE, related_name='destination',null=True)
    prize = models.DecimalField(max_digits=10 , decimal_places=2)


class ticket(models.Model):
    bought_date = models.DateTimeField(auto_now_add=True)
    route = models.ForeignKey(route,on_delete=models.DO_NOTHING , related_name='route')
    level = models.ForeignKey(type,on_delete=models.DO_NOTHING, null=True )  
    Quantity = models.IntegerField(default=1)
    used = models.BooleanField(default=False )
    takeoff_time = models.TimeField(null=True)
    takeoff_date = models.DateField(null=True)
    user = models.ForeignKey(user, on_delete=models.SET_NULL, null=True)




class travelhistory(models.Model):
    ticket = models.ForeignKey(ticket,on_delete=models.DO_NOTHING)
    time = models.DateTimeField(auto_now_add=True)
    vehicle = models.ForeignKey(vehicle, on_delete=models.SET_NULL, null=True)
    
    