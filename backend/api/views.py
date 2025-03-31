from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .permisions import *
from .serializers import *
from .models import *
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import TokenObtainPairSerializer
from django.http import HttpResponse
import sys
sys.path.append("..")
class Ad_dashboard(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ticketSerializer
    queryset = ticket.objects.all()

class sub_dashboard(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsSub]
    serializer_class = vehicleSerializer
    def get_queryset(self):
        users = self.request.user
        return vehicle.objects.filter(branch = users.branch)
class TokenObtain(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


def delete(request):
    route.objects.all().delete()
    return HttpResponse(request)
