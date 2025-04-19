from django.db import models
from user.models import *
from vehicle_management.models import *

import sys
sys.path.append("..")

# Create your models here.
class notification(models.Model):
    class type(models.TextChoices):
        REQUEST = 'r',('request')
        RESPONSE = 's',('response')
    title = models.CharField(max_length= 100 , null=True)
    branch = models.ForeignKey(branch, on_delete=models.CASCADE)
    user = models.ForeignKey(user , on_delete= models.CASCADE, null=True)
    message = models.CharField(max_length=300 )
    time = models.TimeField(auto_now_add= True)
    date = models.DateField(auto_now_add=True)
    read = models.BooleanField(default=False)
    types =models.CharField(max_length=10, choices=type.choices ,default=type.REQUEST)
    class Meta:
        ordering = ['-date','-time']  # Newest messages first

    def __str__(self):
        return f"Notification to {self.user} at {self.time} on {self.date}"
    
class message(models.Model):
    sender = models.ForeignKey(
        user,
        on_delete=models.CASCADE,
        related_name='sent_messages'  # Unique related_name for sender
    )
    receiver = models.ForeignKey(
        user,
        on_delete=models.CASCADE,
        related_name='received_messages'  # Unique related_name for receiver
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']  # Newest messages first

    def __str__(self):
        return f"From {self.sender} to {self.receiver} at {self.timestamp}"