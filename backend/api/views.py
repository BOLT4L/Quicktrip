from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action
from django.utils import timezone
from datetime import timedelta
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated ,AllowAny
from alert.models import notification
from .permisions import *
from .serializers import *
from  vehicle_management.models import *
from  user.models import *
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import TokenObtainPairSerializer
from django.http import HttpResponse
from payment.models import payment
from django.db.models import Q
from rest_framework import status
from .models import *
from django.contrib.auth import update_session_auth_hash
import sys
sys.path.append("..")
class PasswordChangeView(generics.UpdateAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = [IsAuthenticated]
    queryset = user.objects.all()
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = self.get_object()
        user = serializer.update(user, serializer.validated_data)
        
        # Maintain session after password change
        update_session_auth_hash(request, user)
        
        return Response({
            "status": "success",
            "message": "Password updated successfully"
        })
class report(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = travelhistorySerializer
    def get_queryset(self):
        user = self.request.user
        
        if user.user_type == 'a':
            return travelhistory.objects.all()  
        elif user.user_type == 's' and user.branch:
            return travelhistory.objects.filter(branch=user.branch)  # Sub-admin sees only their branch
        else:
            return travelhistory.objects.none()  
class phone_number_search(generics.ListAPIView):
    serializer_class = nidSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        pn = self.kwargs['pn']
        return nidUser.objects.filter(phone_number = pn)

class Fan_search(generics.ListAPIView):
    serializer_class = nidSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        fan = self.kwargs['fan']
        return nidUser.objects.filter(FAN = fan)
    
class branchs(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = branchSerializer
    queryset = branch.objects.all()

class branchDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated,IsAdmin]
    serializer_class = branchSerializer
    queryset = branch.objects.all()

class levels(generics.ListAPIView):
     permission_classes = [IsAuthenticated]
     serializer_class = levelSerializer
     queryset = type.objects.all()

class routes_sub(generics.ListCreateAPIView):
     permission_classes = [AllowAny]
     serializer_class = routeSerializer
     queryset = route.objects.all()
class routes(generics.ListAPIView):
     permission_classes = [IsAuthenticated,IsSub]
     serializer_class = routeSerializer
     queryset = route.objects.all()
class detailRoutes(generics.RetrieveUpdateDestroyAPIView):
     permission_classes = [IsAuthenticated,IsSub,IsBranch]
     serializer_class = routeSerializer
     queryset = route.objects.all()
class Staffs(generics.ListCreateAPIView):
     permission_classes = [AllowAny]
     serializer_class = userSerializer
     queryset = user.objects.filter(user_type = 's')
class usertravel(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = UsertravelSerializer
    queryset = user.objects.exclude(travel_history__isnull = True)

class ad_notif(generics.ListCreateAPIView):
     permission_classes = [AllowAny]
     serializer_class = notificationSerilalizer
     def get_queryset(self):
        id = self.kwargs['id']
        return notification.objects.filter(user = id)
    
class messages(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        id = self.kwargs['id']
        return message.objects.filter(
            models.Q(sender=id) | models.Q(receiver=id)
        ).order_by('-timestamp')

class ad_editnotif(generics.RetrieveUpdateDestroyAPIView):
     permission_classes = [AllowAny]
     serializer_class = notificationSerilalizer
     queryset = notification.objects.all()


class driver(generics.ListCreateAPIView):
     permission_classes = [AllowAny]
     serializer_class = userSerializer
     queryset = user.objects.all()



class sub_dashboard(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsSub]
    serializer_class = vehicleSerializer
    def get_queryset(self):
        users = self.request.user
        return vehicle.objects.filter(branch = users.branch)
class TokenObtain(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

class sub_travels(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated,IsSub,IsBranch]
    serializer_class = travelhistorySerializer
    def get_queryset(self):
        route_id = self.kwargs['rid']
        return travelhistory.objects.filter( ticket__route = route_id)
     
class staffListAD(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = userSerializer
    def get_queryset(self):
        branch_id = self.kwargs['bid']
        return user.objects.filter(branch = branch_id)
 
class addtraveller(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = addtraveller
    queryset = user.objects.all()
    
class other_cred(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = credSerializer
    queryset = credentials.objects.all()



class userDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny] 
    serializer_class = UserSerializer
    queryset = user.objects.all()
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True 
        return super().update(request, *args, **kwargs)
    
def delete(request):
    route.objects.all().delete()
    return HttpResponse(request)
class getuser(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = userSerializer
    def get_queryset(self):
        phone_number = self.kwargs['phonenumber']
        return user.objects.filter(phone_number = phone_number)

class sub_route(generics.ListAPIView):
    permission_classes = [IsAuthenticated,IsSub, IsBranch]
    serializer_class = routeSerializer
    def get_queryset(self):
        users = self.request.user
        if users.user_type == 'a':
            return route.objects.all()  
        elif users.user_type == 's' and users.branch:
            return route.objects.filter(first_destination=users.branch)  
        else:
            return route.objects.none()  
class buyticket(generics.CreateAPIView):
    serializer_class = ticketSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        branch_id = self.kwargs['bid']
        return ticket.objects.filter(route__first_destination = branch_id)
class payments(generics.ListAPIView):
    serializer_class = paymentSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        user = self.request.user
        
        if user.user_type == 'a':
            return payment.objects.all()  
        elif user.user_type == 's' and user.branch:
            return payment.objects.filter(branch=user.branch) 
        else:
            return  payment.objects.none()  

class driver_payments(generics.ListAPIView):
    serializer_class = paymentSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        users = self.request.user
        
        if users.user_type == 'a':
            return payment.objects.all()  
        elif users.user_type == 's' and users.branch:
            return payment.objects.filter(branch=users.branch,user__user_type = "d") 
        return  payment.objects.none()  

class vehicles(generics.ListAPIView):
    serializer_class = vehiclesSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        
        if user.user_type == 'a':
            return vehicle.objects.all()  
        elif user.user_type == 's' and user.branch:
            return vehicle.objects.filter(branch=user.branch)  # Sub-admin sees only their branch
        else:
            return vehicle.objects.none()  

class vehiclesDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = vehiclesSerializer
    permission_classes = [IsAuthenticated]
    queryset = vehicle.objects.all()


class VehicleViewSet(generics.ListCreateAPIView):
    queryset = vehicle.objects.all()
    serializer_class = vehicleSerializer
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]
    def get_queryset(self):
        branch_id = self.kwargs['bid']
        return vehicle.objects.filter(branch = branch_id)

    @action(detail=True, methods=['post'])
    def update_location(self, request, pk=None):
        vehicle = self.get_object()
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        
        if latitude and longitude:
            location = Location.objects.create(
                latitude=latitude,
                longitude=longitude
            )
            vehicle.location = location
            vehicle.is_active = True
            vehicle.save()
            return Response({'status': 'location updated'})
        return Response({'status': 'invalid data'}, status=400)

    @action(detail=False, methods=['get'])
    def active_vehicles(self, request):
        active_threshold = timezone.now() - timedelta(minutes=5)
        active_vehicles = vehicle.objects.filter(
            last_updated__gte=active_threshold,
            is_active=True
        )
        serializer = self.get_serializer(active_vehicles, many=True)
        return Response(serializer.data)