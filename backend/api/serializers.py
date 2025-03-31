from user.models import *
from booking.models import *
from rest_framework import serializers
from vehicle_management.models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
import sys
sys.path.append("..")


class userSerializer(serializers.ModelSerializer):
    class Meta :
        model = user
        fields = '__all__'
        extra_kwargs = {'password':{"write_only": True}}


class branchSerializer(serializers.ModelSerializer):
    class Meta :
        model = branch
        fields = '__all__'
       

class vehicleSerializer(serializers.ModelSerializer):
    class Meta : 
        model = vehicle
        fields = '__all__'


class TokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user) 
        token['role'] = user.user_type  # Custom User model field (e.g., 'ADMIN'/'SUB_ADMIN')
        token['user_id'] = user.id

        return token
class ticketSerializer(serializers.Serializer):
    class Meta :
        model = ticket
        fields = "__all__"