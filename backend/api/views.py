from django.shortcuts import render
from rest_framework import generics
import datetime
import requests
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from django.utils import timezone
from datetime import timedelta
from rest_framework.response import Response
from rest_framework.views import APIView    
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
from django.http import HttpResponse
from django.db.models import Sum
from datetime import datetime, timedelta
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from io import BytesIO 
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import update_session_auth_hash
import sys
sys.path.append("..")
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Transaction
from django.views.decorators.http import require_POST
import json
from decimal import Decimal
from backend.config import send_twilio_message

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
def home(request):
    return render(request, 'home.html')

def calculate_distance(lat1, lon1, lat2, lon2):
     
        lat1 = float(lat1) if isinstance(lat1, Decimal) else lat1
        lon1 = float(lon1) if isinstance(lon1, Decimal) else lon1
        lat2 = float(lat2) if isinstance(lat2, Decimal) else lat2
        lon2 = float(lon2) if isinstance(lon2, Decimal) else lon2
        
        # Haversine formula implementation
        R = 6371  # Earth radius in km
        dLat = math.radians(lat2 - lat1)
        dLon = math.radians(lon2 - lon1)
        a = (math.sin(dLat/2) * math.sin(dLat/2) +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dLon/2) * math.sin(dLon/2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c
@csrf_exempt
@require_POST
def send_alert(request):
    try:
        data = json.loads(request.body)
        vehicle_id = data.get('vehicle_id')
        message = data.get('message')
        user_id = data.get('user_id')
        vehicles = vehicle.objects.get(pk=vehicle_id)
        vehicle_location = vehicles.location
        
        # Find nearest branch
        nearest_branch = None
        min_distance = float('inf')
        
        for branch in Branch.objects.all():
            branch_location = branch.location
            distance = calculate_distance(
                vehicle_location.latitude, vehicle_location.longitude,
                branch_location.latitude, branch_location.longitude
            )
            
            if distance < min_distance:
                min_distance = distance
                nearest_branch = branch
        
        # Create notification
        notifications = notification.objects.create(
            title="Vehicle Alert",
            branch=nearest_branch,
            user_id=user_id,
            vehicle=vehicles,
            message=message,
            notification_type=notification.Type.ALERT
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Alert sent to nearest branch',
            'branch': nearest_branch.name,
            'distance': f"{min_distance:.2f} km"
        })
    
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)
@csrf_exempt  # Temporarily disable CSRF for testing (remove in production)
def payment_form(request):
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            amount = data.get('amount', 100.00)   
            
            return render(request, 'home.html', {'amount': amount})

            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    # GET request - render template
    return render(request, 'home.html', {'amount': 100.00})


@csrf_exempt  # Allow external POST from Chapa's callback
def payment_callback(request):
    if request.method == 'POST':
        data = request.POST
        transaction_id = data.get('tx_ref')
        amount = data.get('amount')
        status = data.get('status')  # 'success', 'failed', etc.
        Transaction.objects.create(
            transaction_id=transaction_id,
            amount=amount,
            status=status
        )
 
        return JsonResponse({'message': 'Callback received'})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

def success_page(request):
    transaction_id = request.GET.get('tx_ref')

    transaction = Transaction.objects.filter(transaction_id=transaction_id).first()
    return render(request, 'next.html', {'transaction': transaction})


class NotificationListViews(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return notification.objects.filter(user=self.request.user).order_by('-date', '-time')

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def mark_notification_as_read(request, pk):
    try:
        notifications = notification.objects.get(pk=pk, user=request.user)
        if not notifications.read:
            notifications.read = True
            notifications.save()
            return Response({
                'status': 'success',
                'unread_count': notification.objects.filter(user=request.user, read=False).count()
            })
        return Response({'status': 'already read'})
    except notification.DoesNotExist:
        return Response({'status': 'not found'}, status=404)

@api_view(['POST']) 
def mark_all_notifications_read(request):
    updated_count = notification.objects.filter(
        user=request.user, 
        read=False
    ).update(read=True)
    
    return Response({
        'status': 'success',
        'marked_read_count': updated_count,
        'unread_count': 0
    })

class PasswordChangeView(generics.UpdateAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = self.get_object()
        user = serializer.update(user, serializer.validated_data)
        
        update_session_auth_hash(request, user)
        
        return Response({
            "status": "success",
            "message": "Password updated successfully"
        })
class report(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = travelhistorySerializer
    def get_queryset(self):
        user = self.request.user
        
        if user.user_type == 'a':
            return travelhistory.objects.all()  
        elif user.user_type == 's' and user.branch:
            return travelhistory.objects.filter(branch=user.branch)  # Sub-admin sees only their branch
        else:
            return travelhistory.objects.none()  
 # OTP 
class SendOTPView(generics.CreateAPIView):
    queryset = OTP.objects.all()
    serializer_class = OTPSerializer 
    permission_classes = [AllowAny]
class OTPVerifyView(generics.GenericAPIView):
    serializer_class = OTPSerializer

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        code = request.data.get('code')
        
        if not phone_number or not code:
            return Response(
                {"detail": "Both phone_number and code are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            otp = OTP.objects.get(
                phone_number=phone_number,
                code=code
            )
            
            # Check if OTP is expired (5 minutes)
            if otp.created_at < timezone.now() - timedelta(minutes=15):
                otp.delete()
                return Response(
                    {"detail": "OTP has expired"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # OTP is valid
            otp.delete()  # Delete after successful verification
            return Response(
                {"detail": "OTP verified successfully"},
                status=status.HTTP_200_OK
            )
            
        except OTP.DoesNotExist:
            return Response(
                {"detail": "Invalid OTP"},
                status=status.HTTP_400_BAD_REQUEST
            )   

class RequestOTPView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({'error': 'Phone number required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(phone_number=phone_number)
            otp = OTP.objects.create(phone_number=phone_number)
            return Response({'message': 'OTP sent successfully'})
        except User.DoesNotExist:
            return Response({'error': 'User with this phone number does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
class ResetPasswordView(APIView):
    def post(self, request):
        from django.utils import timezone
        from datetime import timedelta

        # Clear expired OTPs first
        valid_period = timezone.now() - timedelta(minutes=15)
        OTP.objects.filter(created_at__lt=valid_period).delete()

        phone_number = request.data.get('phone_number')
        otp_code = request.data.get('otp')
        new_password = request.data.get('new_password')

        if not all([phone_number, otp_code, new_password]):
            return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            otp = OTP.objects.filter(
                phone_number=phone_number,
                code=otp_code,
                created_at__gte=timezone.now() - timedelta(minutes=15)
            ).latest('created_at')

            user = User.objects.get(phone_number=phone_number)
            user.set_password(new_password)
            user.save()

            return Response({'message': 'Password reset successful'})
        except OTP.DoesNotExist:
            return Response({'error': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

def normalize_phone(phone):
    return phone.replace(" ", "").replace("-", "").lstrip("0").replace("+251", "")

def format_phone_number(phone_number):
    # Remove all non-digit characters
    cleaned = ''.join(filter(str.isdigit, phone_number))
    
    # Get the last 9 digits (assuming Ethiopian numbers are 9 digits after +251)
    last_9 = cleaned[-9:]
    
    # If the number starts with '0' (local format), remove it
    if last_9.startswith('0'):
        last_9 = last_9[1:]
    
    # Ensure it's exactly 9 digits (for Ethiopian numbers)
    if len(last_9) != 9:
        raise ValueError("Invalid phone number length after formatting")
    
    return f"+251{last_9}"

class RegisterUserView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        # Normalize and validate phone number
        raw_phone = request.data.get("phone_number", "")
        phone = normalize_phone(raw_phone)
        if not phone:
            return Response({"detail": "Valid phone number is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        phone = "+251" + phone  # Add country code
        password = request.data.get("password")
        otp = request.data.get("otp")
        nid = request.data.get("nid")
        try:  
            message_body = f"""
            QUICKTRIP OTP

            Hello,

            Your Current Password is: {password}

            Please Change Password after Login
            """
            send_twilio_message(format_phone_number(phone), message_body)
            print(f"Password sent to {phone}")
        except Exception as e:
            print(f"Error sending Message: {e}")
        # Validate required fields
        if not all([phone, password, otp]):
            return Response(
                {"detail": "Phone, password, and OTP are required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verify OTP (latest OTP for that phone within 15 minutes)
        try:
            otp_obj = OTP.objects.filter(
                phone_number=phone,
                code=otp,
                created_at__gte=timezone.now() - timedelta(minutes=15)
            ).latest("created_at")
        except OTP.DoesNotExist:
            return Response(
                {"detail": "Invalid or expired OTP"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if user already exists
        if User.objects.filter(phone_number=phone).exists():
            return Response(
                {"detail": "User with this phone number already exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create user
        user_data = {
            'phone_number': phone,
            'password': password,
            'user_type': 'u'  # Default to regular user
        }

        try:
            user = User.objects.create_user(**user_data)
            
            # Associate Fayda/NID if provided
            if nid:
                try:
                    fayda_user = nidUser.objects.get(id=nid)
                    user.nid = fayda_user
                    user.save()
                except nidUser.DoesNotExist:
                    return Response(
                        {"detail": "Invalid Fayda ID"}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Delete the used OTP
            otp_obj.delete()

            return Response(
                {
                    "message": "User registered successfully",
                    "user_id": user.id,
                    "phone_number": user.phone_number,
                    "nid_associated": bool(user.nid)
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"detail": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
class phone_number_search(generics.ListAPIView):
    serializer_class = nidSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        pn = self.kwargs['pn']
        return nidUser.objects.filter(phone_number = pn)

class Fan_search(generics.ListAPIView):
    serializer_class = nidSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        fan = self.kwargs['fan']
        return nidUser.objects.filter(FAN = fan)
class fan_ticket_search(generics.ListAPIView):
    serializer_class = nidSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        tid = self.kwargs['tid']
        tickets = ticket.objects.get(id = tid)
        user = tickets.user

        return nidUser.objects.filter(id = user.nid.id)  
class branchs(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = branchSerializer
    queryset = Branch.objects.all()

class branchDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated,IsAdmin]
    serializer_class = branchSerializer
    queryset = Branch.objects.all()

class levels(generics.ListAPIView):
     permission_classes = [IsAuthenticated]
     serializer_class = levelSerializer
     queryset = type.objects.all()

class routes_sub(generics.ListCreateAPIView):
     permission_classes = [IsAuthenticated]
     serializer_class = routeSerializer
     queryset = route.objects.all()
class routes(generics.ListAPIView):
     permission_classes = [AllowAny]
     serializer_class = routeSerializer
     queryset = route.objects.all()
class detailRoutes(generics.RetrieveUpdateDestroyAPIView):
     permission_classes = [IsAuthenticated,IsSub,IsBranch]
     serializer_class = routeSerializer
     queryset = route.objects.all()
class Staffs(generics.ListCreateAPIView):
     permission_classes = [AllowAny]
     serializer_class = usersSerializer
     queryset = User.objects.filter(user_type = 's')

class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    lookup_field = 'id'
    
class EmployeeDetailView(generics.RetrieveUpdateAPIView):
    queryset = employeeDetail.objects.all()
    serializer_class = EmployeeDetailSerializer
    lookup_field = 'id'

class VehicleEditView(generics.RetrieveUpdateAPIView):
    queryset = vehicle.objects.all()
    serializer_class = vehicleSerializer
    lookup_field = 'id'
class RouteEditView(generics.RetrieveUpdateDestroyAPIView):
    queryset = route.objects.all()
    permission_classes = [AllowAny]
    serializer_class = routeSerializer
    lookup_field = 'id'
    def delete(self, request, *args, **kwargs): 
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({"status": "success"})
class BranchsListView(generics.ListAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated]
     
class usertravel(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = UsertravelSerializer
    queryset = User.objects.exclude(travel_history__isnull = True)

class ad_notif(generics.ListCreateAPIView):
     permission_classes = [AllowAny]
     serializer_class = notificationSerilalizer
     def get_queryset(self):
        id = self.kwargs['id']
        return notification.objects.filter(user = id)
    
class messages(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        id = self.kwargs['id']
        return message.objects.filter(
            models.Q(sender=id) | models.Q(receiver=id)
        ).order_by('-timestamp')
class messages_Add(generics.ListCreateAPIView):
    serializer_class = MessageaddSerializer
    permission_classes = [AllowAny]
    queryset =message.objects.all()
class MarkMessagesReadView(generics.UpdateAPIView):
    serializer_class = MessageSerializer
    queryset = message.objects.all()
    
    def update(self, request, *args, **kwargs):
        message_ids = request.data.get('message_ids', [])
        
        if not message_ids:
            return Response(
                {"error": "No message IDs provided"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Filter messages that belong to the current user as receiver
        messages = self.get_queryset().filter(
            Q(id__in=message_ids) & 
            Q(receiver=request.user) & 
            Q(read=False)
        )
        
        updated_count = messages.update(read=True)
        
        return Response(
            {"success": f"Marked {updated_count} messages as read"},
            status=status.HTTP_200_OK
        )

class MarkConversationReadView(generics.UpdateAPIView):
    serializer_class = MessageSerializer
    queryset = message.objects.all()
    
    def update(self, request, *args, **kwargs):
        sender_id = kwargs.get('sender_id')
        
        # Mark all unread messages from this sender to current user
        messages = self.get_queryset().filter(
            Q(sender_id=sender_id) & 
            Q(receiver=request.user) & 
            Q(read=False)
        )
        
        updated_count = messages.update(read=True)
        
        return Response(
            {"success": f"Marked {updated_count} messages as read"},
            status=status.HTTP_200_OK
        )
class ad_editnotif(generics.RetrieveUpdateDestroyAPIView):
     permission_classes = [AllowAny]
     serializer_class = notificationSerilalizer
     queryset = notification.objects.all()


class driver(generics.ListCreateAPIView):
     permission_classes = [AllowAny]
     serializer_class = userSerializer
     queryset = User.objects.filter(user_type = 'd')


class adddriver(generics.ListCreateAPIView):
     permission_classes = [AllowAny]
     serializer_class = adddriverSerializer
     queryset = User.objects.filter(user_type = 'd')



class sub_dashboard(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsSub]
    serializer_class = vehicleSerializer
    def get_queryset(self):
        users = self.request.user
        return vehicle.objects.filter(branch = users.branch)
class recent(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = travelhistorySerializer
    def get_queryset(self):
        users = self.request.user
        return travelhistory.objects.filter(user = users.id)
class driver_recent(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = travelhistorySerializer
    def get_queryset(self):
        users = self.kwargs['uid']
        return travelhistory.objects.filter(vehicle__user = users)
class ExitSlipListView(generics.ListAPIView):
    serializer_class = ExitSlipSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        id = self.kwargs['driver']
        return ExitSlip.objects.filter(vehicle__user=id,status = 'c'  ).order_by('-departure_time')
class ExitSlipListCreateView(generics.ListCreateAPIView):
    serializer_class = ExitSlipSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        id = self.kwargs['driver']
        return ExitSlip.objects.filter(vehicle__user=id, status = 'a').order_by('-departure_time')
   
class ExitSlipDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExitSlip.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ExitSlipSerializer
class TokenObtain(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

class sub_travels(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated,IsSub,IsBranch]
    serializer_class = travelhistorySerializer
    def get_queryset(self):
        route_id = self.kwargs['rid']
        return travelhistory.objects.filter( ticket__route = route_id)
     
class staffListAD(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = userSerializer
    def get_queryset(self):
        branch_id = self.kwargs['bid']
        return User.objects.filter(branch = branch_id)
 
class addtraveller(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = addtraveller
    queryset = User.objects.all()
    
class other_cred(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = credSerializer
    queryset = credentials.objects.all()



class userDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated] 
    serializer_class = UserSerializer
    queryset = User.objects.all()
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True 
        return super().update(request, *args, **kwargs)
    
def delete(request):
    route.objects.all().delete()
    return HttpResponse(request)
class getuser(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = userSerializer
    def get_queryset(self):
        phone_number = self.kwargs['phonenumber']
        return User.objects.filter(phone_number = phone_number)

class sub_route(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = routeSerializers
    def get_queryset(self):
        users = self.request.user
        if users.user_type == 'a':
            return route.objects.all()  
        elif users.user_type == 's' and users.branch:
            return route.objects.filter(first_destination=users.branch)  
        else:
            return route.objects.none()  
class station_route(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = routeSerializer
    def get_queryset(self):
        sid = self.kwargs['sid']
        return route.objects.filter(first_destination__id = sid)
      
class tickets(generics.ListAPIView):
    serializer_class = ticketSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        users = self.request.user
        if users.user_type == 'a':
            return ticket.objects.all(used = False)  
        elif users.user_type == 's' and users.branch:
            return ticket.objects.filter(route__first_destination=users.branch, used = False)  
        else:
            return ticket.objects.filter(user = users.id, used = False) 
        
class buyticket(generics.CreateAPIView):
    serializer_class = buyticketSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        users = self.request.user
        if users.user_type == 'a':
            return ticket.objects.all()  
        elif users.user_type == 's' and users.branch:
            return ticket.objects.filter(route__first_destination=users.branch)  
        elif users.user_type == 'u' and users.branch:
            return ticket.objects.filter(route__first_destination=users.branch)  
        else:
            return route.objects.none()  
class payments(generics.ListCreateAPIView):
    serializer_class = paymentSerializer
    permission_classes = [AllowAny]
 
    def get_queryset(self):
        users = self.request.user
        if users.user_type == 'a':
            return payment.objects.all()  
        elif users.user_type == 's' and users.branch:
            return payment.objects.filter(branch=users.branch)  
        else:
            return route.objects.none()
    
class addpayments(generics.CreateAPIView):
    serializer_class = addpaymentSerializer
    permission_classes = [IsAuthenticated]
    queryset = payment.objects.all()
    
class driver_payments(generics.ListAPIView):
    serializer_class = paymentSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        users = self.request.user
        
        if users.user_type == 'a':
            return payment.objects.filter(user__user_type = "d",vehicle__plate_number__isnull = False)
        elif users.user_type == 's' and users.branch:
            return payment.objects.filter(branch=users.branch,user__user_type = "d",vehicle__plate_number__isnull = False) 
        return  payment.objects.none()  

class vehicles(generics.ListCreateAPIView):
    serializer_class = vehiclesSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'a':
            return vehicle.objects.all()  
        elif user.user_type == 's' and user.branch:
            return vehicle.objects.filter(branch=user.branch)
        elif user.user_type == 'u' and user.user_type == 'd' and user.branch:
            return vehicle.objects.all()
        else:
            return vehicle.objects.none()  

class vehicleUser(generics.ListCreateAPIView):
    serializer_class = vehiclesSerializer
    permission_classes = [AllowAny]
    queryset = vehicle.objects.all()
class vehiclesDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = vehiclesSerializer
    permission_classes = [IsAuthenticated]
    queryset = vehicle.objects.all()
class VehicleLocation(generics.ListAPIView):
    serializer_class = VehicleLocationSerializer
    permission_classes = [AllowAny]
    queryset = vehicle.objects.all()
class driver_vehicle(generics.ListAPIView):
    serializer_class = vehiclesSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        d_id = self.kwargs['did']
        return vehicle.objects.filter(user = d_id)

class VehicleViewSet(generics.ListCreateAPIView):
    queryset = vehicle.objects.all()
    serializer_class = vehicleSerializer
    permission_classes = [IsAuthenticated]
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
    
@api_view(['PATCH'])
@permission_classes([AllowAny])
def pay_driver(request, id):
    try:
        # Get payment object
        try:
            instance = payment.objects.get(id=id)
        except payment.DoesNotExist:
            return Response({"error": "Payment not found."}, status=404)

        # Update payment status
        instance.status = payment.status_type.COMPLETED
        instance.save(update_fields=['status'])  # ensures DB commit

        user = instance.user
        branch = instance.branch
        vh = instance.vehicle

        if not branch or not vh:
            return Response({"error": "Branch or vehicle missing in payment."}, status=400)

        # Mark all related unread notifications as read
        notif = notification.objects.filter(branch=branch, vehicle=vh, read=False)
        notif.update(read=True)
        notifs = notification.objects.create(
            title="Journey Started",
            branch=vh.branch,
            user=vh.user,
            vehicle=vh,
            message="Your journey has been approved and payment has been made. You can start your journey now.",
            notification_type=notification.Type.RESPONSE
            # time and date will be auto set
        )
        # Check vehicle route
        route = getattr(vh, 'route', None)
        if not route:
            return Response({"error": "Vehicle has no route assigned."}, status=400)

        # Determine destination
        if route.first_destination != branch:
            to_location = route.first_destination
        elif route.last_destination != branch:
            to_location = route.last_destination
        else:
            return Response({"error": "No valid destination found in route."}, status=400)

        # Create ExitSlip
        exit_slip = ExitSlip.objects.create(
            vehicle=vh,
            driver=user,
            from_location=branch,
            to_location=to_location,
            departure_time=timezone.now(),
            passenger_count=vh.sit_number,
            status=ExitSlip.Status.APPROVED,
            qr_code=f"EXIT-{id}-{vh.plate_number}"
        )

        q = Queues.objects.filter(vehicle = vh)
        q.status = 'departed'
        q.save()
        # Serialize and return updated payment
        serializer = addpaymentSerializer(instance)
        vh.tracking = True
        vh.save()
        return Response(serializer.data)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({"error": str(e)}, status=500)
class UserDeactivateAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = userSerializer
    permission_classes = [IsAuthenticated]   
    lookup_field = 'id'

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()       
        if instance == request.user:
            return Response(
                {"detail": "You cannot deactivate yourself."},
                status=status.HTTP_403_FORBIDDEN
            )
            
        instance.is_active = False
        instance.save()
       
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
def monthly_revenue_report(request):
    
    today = datetime.now()
    first_day = today.replace(day=1)
    last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
   
    all_payments = payment.objects.filter(
        date__range=[first_day, last_day]
    ).select_related('branch', 'user', 'vehicle').order_by('date')
    
    # Get completed income payments for totals
    income_payments = all_payments.filter(
        status='c',  # completed
        types='i'    # income
    )
    
    
    total_revenue = income_payments.aggregate(Sum('amount'))['amount__sum'] or 0
    branch_totals = income_payments.values('branch__name').annotate(total=Sum('amount'))
   
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 800, f"Monthly Revenue Report - {today.strftime('%B %Y')}")
    p.setFont("Helvetica", 12)
    p.drawString(100, 780, f"Total Revenue: ${total_revenue:.2f}")
    
    # Revenue by Branch
    y_position = 750
    p.drawString(100, y_position, "Revenue by Branch:")
    y_position -= 20
    
    for branch in branch_totals:
        p.drawString(120, y_position, f"{branch['branch__name']}: ${branch['total']:.2f}")
        y_position -= 20
    
    # Payment Details Table
    y_position -= 40
    p.drawString(100, y_position, "All Payments:")
    y_position -= 30
    
    # Prepare table data
    table_data = [
        ['Date', 'Type', 'Status', 'Branch', 'Amount', 'Transaction ID', 'User', 'Vehicle']
    ]
    
    for payments in income_payments:
        table_data.append([
            payments.date.strftime('%Y-%m-%d'),
            payments.get_types_display(),
            payments.get_status_display(),
            payments.branch.name if payments.branch else 'N/A',
            f"${payments.amount:.2f}",
            payments.transaction_id,
            f"{payments.user.employee.Fname} {payments.user.employee.Lname}" if payments.user else 'N/A',
            payments.vehicle.plate_number if payments.vehicle else 'N/A'
        ])
    
    # Create table
    table = Table(table_data, colWidths=[70, 50, 50, 70, 50, 90, 80, 70])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('FONTSIZE', (0,1), (-1,-1), 8),
    ]))
    
    # Draw table on canvas
    table.wrapOn(p, 400, 200)
    table.drawOn(p, 40, y_position - len(all_payments)*20 - 50)
    
    p.showPage()
    p.save()
    
    # Prepare response
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="monthly_report_{today.strftime("%Y_%m")}.pdf"'
    return response
def monthly_tax_report(request):
    
    today = datetime.now()
    first_day = today.replace(day=1)
    last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
   
    all_payments = payment.objects.filter(
        date__range=[first_day, last_day]
    ).select_related('branch', 'user', 'vehicle').order_by('date')
    
    # Get completed income payments for totals
    tax_payments = all_payments.filter(
        status='c', 
        types ='e'
    )
    
    
    total_revenue = tax_payments.aggregate(Sum('amount'))['amount__sum'] or 0
    branch_totals = tax_payments.values('branch__name').annotate(total=Sum('amount'))
   
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 800, f"Monthly Expense Report - {today.strftime('%B %Y')}")
    p.setFont("Helvetica", 12)
    p.drawString(100, 780, f"Total Expense: ${total_revenue:.2f}")
    
    # Revenue by Branch
    y_position = 750
    p.drawString(100, y_position, "Expense by Branch:")
    y_position -= 20
    
    for branch in branch_totals:
        p.drawString(120, y_position, f"{branch['branch__name']}: ${branch['total']:.2f}")
        y_position -= 20
    
    # Payment Details Table
    y_position -= 40
    p.drawString(100, y_position, "All Payments:")
    y_position -= 30
    
    # Prepare table data
    table_data = [
        ['Date', 'Type', 'Status', 'Branch', 'Amount', 'Transaction ID', 'User', 'Vehicle']
    ]
    
    for payments in tax_payments:
        table_data.append([
            payments.date.strftime('%Y-%m-%d'),
            payments.get_types_display(),
            payments.get_status_display(),
            payments.branch.name if payments.branch else 'N/A',
            f"${payments.amount:.2f}",
            payments.transaction_id,
            f"{payments.user.employee.Fname} {payments.user.employee.Lname}" if payments.user else 'N/A',
            payments.vehicle.plate_number if payments.vehicle else 'N/A'
        ])
    
    # Create table
    table = Table(table_data, colWidths=[70, 50, 50, 70, 50, 90, 80, 70])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('FONTSIZE', (0,1), (-1,-1), 8),
    ]))
    
    # Draw table on canvas
    table.wrapOn(p, 400, 200)
    table.drawOn(p, 40, y_position - len(all_payments)*20 - 50)
    
    p.showPage()
    p.save()
    
    # Prepare response
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="monthly_tax_report_{today.strftime("%Y_%m")}.pdf"'
    return response
def Passengers_report(request):
    
    today = datetime.now()
    first_day = today.replace(day=1)
    last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
   
    all_user =travelhistory.objects.filter(
      time__range=[first_day, last_day]
    ).select_related('branch','user', 'vehicle','payment','ticket' ).order_by('time')
    
    total_passenger = all_user.count() or 0
    
   
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 800, f"Monthly Passenger Report - {today.strftime('%B %Y')}")
    p.setFont("Helvetica", 12)
    p.drawString(100, 780, f"Total Passengers : {total_passenger}")
    y_position = 750
    y_position -= 20
    
    
    
    # Payment Details Table
    y_position -= 40
    p.drawString(100, y_position, "All Passengers:")
    y_position -= 30
    
    # Prepare table data
    table_data = [
        ['Date', 'First Name', 'Last Name', 'Branch', 'Amount', 'Transaction ID', 'Driver', 'Vehicle']
    ]
    
    for users in all_user:
        table_data.append([
            users.time.strftime('%Y-%m-%d'),
            users.user.nid.Fname,
            users.user.nid.Lname,
            users.branch.name if users.branch else 'N/A',
            f"${users.payment.amount:.2f}",
            users.payment.transaction_id,
            f"{users.vehicle.user.employee.Fname} {users.vehicle.user.employee.Lname}" if users.vehicle.user else 'N/A',
            users.vehicle.plate_number if users.vehicle else 'N/A'
        ])
    
    # Create table
    table = Table(table_data, colWidths=[70, 70, 70, 70, 50, 90, 80, 70])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('FONTSIZE', (0,1), (-1,-1), 8),
    ]))
    
    # Draw table on canvas
    table.wrapOn(p, 400, 200)
    table.drawOn(p, 40, y_position - len(all_user)*20 - 50)
    
    p.showPage()
    p.save()
    
    # Prepare response
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="passengers_report_{today.strftime("%Y_%m")}.pdf"'
    return response

def vehicle_report_pdf(request):
   
    vehicles = vehicle.objects.select_related(
        'branch', 'user', 'types', 'location', 'route'
    ).order_by('plate_number')
    
    # Create PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # PDF Header
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 800, "Active Vehicle Report")
    p.setFont("Helvetica", 12)
    p.drawString(100, 780, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    p.drawString(100, 760, f"Total Vehicles: {vehicles.count()}")
    
    # Vehicle Details Table
    y_position = 730
    p.drawString(100, y_position, "Vehicle Details:")
    y_position -= 20
    
    # Prepare table data
    table_data = [
        ['Plate', 'Name', 'Model', 'Type', 'Branch', 'Driver', 'Seats', 'Year', 'Insurance']
    ]
    
    for v in vehicles:
        table_data.append([
            v.plate_number,
            v.name,
            v.Model,
            v.types.detail if v.types else 'N/A',
            v.branch.name if v.branch else 'N/A',
            f"{v.user.employee.Fname} {v.user.employee.Lname}" if v.user else 'N/A',
            str(v.sit_number),
            v.year if v.year else 'N/A',
            v.insurance_date.strftime('%Y-%m-%d') if v.insurance_date else 'None'
        ])
    
    # Create table
    table = Table(table_data, colWidths=[60, 70, 70, 60, 70, 80, 40, 40, 60])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('FONTSIZE', (0,1), (-1,-1), 8),
    ]))
    
    # Draw table on canvas
    table.wrapOn(p, 400, 200)
    table.drawOn(p, 20, y_position - len(vehicles)*20 - 50)
    
    p.showPage()
    p.save()
    
    # Prepare response
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="vehicle_report.pdf"'
    return response

#Alerting view 

class CheckQueueStatus(APIView):
    permission_classes = [AllowAny]
    def get(self, request, vehicle_id):
        try:
            queue = Queues.objects.filter(vehicle_id=vehicle_id).exclude(status='DEPARTED').latest('date', 'time')
            return Response({
                "vehicle_id": vehicle_id,
                "status": queue.status,
                "position": queue.position,
                "current_passengers": queue.current_passengers
            })
        except Queues.DoesNotExist:
            return Response({"message": "Vehicle is not in any active queue."})
        

class LeaveQueueView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = leaveToQueueSerializer
    def post(self, request,vehicle_id, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vehicle_id = serializer.validated_data['vehicle_id']
        message = Queues.leave_queue(vehicle_id)
        return Response({"message": message}, status=status.HTTP_200_OK)
    

class AddToQueueGenericView(generics.CreateAPIView):
    serializer_class = AddToQueueSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        branch_id = serializer.validated_data['branch_id']
        user_id = serializer.validated_data['user_id']
        vehicle.objects.filter(user__id=user_id).update(tracking=False)
        ExitSlip.objects.filter(vehicle__user__id=user_id).update(status='c')
        queue, message = Queues.add_to_queue(user_id, branch_id)
        if queue:
            return Response({
                "message": message,
                "queue_id": queue.id,
                "position": queue.position,
                "status": queue.status
            }, status=status.HTTP_201_CREATED)
        return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)

class queueRetrieveView(generics.ListAPIView):
    serializer_class = RetrieveQueueSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        bid = self.kwargs['bid']
        return Queues.objects.filter(branch__id = bid)
    
class BoardPassengerView(GenericAPIView):
    serializer_class = BoardingSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ticket_id = serializer.validated_data['ticket_id']
        today = timezone.now().date()
        
       
        try:
            user_ticket = ticket.objects.get(id=ticket_id, used = False)
            user = user_ticket.user
           
        except ticket.DoesNotExist:
            return Response({"error": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get matching queue
        
        try:
            matching_queue = Queues.objects.get(
                date=today,
                status__in=['WAITING', 'BOARDING'],
                dest=user_ticket.route.last_destination,
                level=user_ticket.level
            )
        except Queues.DoesNotExist:
            return Response({"error": "No active queue matches ticket's level and destination."}, status=status.HTTP_404_NOT_FOUND)

        # Check that the vehicle's route matches the ticket route
        if matching_queue.vehicle.route != user_ticket.route:
            return Response({"error": "Ticket route and vehicle route do not match."}, status=status.HTTP_400_BAD_REQUEST)

        # Board the passenger (increment quantity)
        pas = matching_queue.current_passengers + user_ticket.Quantity
        if pas >= matching_queue.vehicle.sit_number-1:
            matching_queue.status = 'FULL'
            matching_queue.current_passengers = pas
            matching_queue.save()
           # matching_queue.status = 'DEPARTED'
            # matching_queue.save()

            next_q = Queues.objects.filter(
                date=today,
                branch=matching_queue.branch,
                dest=matching_queue.dest,
                level=matching_queue.level,
                position__gt=matching_queue.position,
                status='WAITING'
            ).order_by('position').first()

            if next_q:
                next_q.status = 'BOARDING'
                next_q.position = 1
                next_q.save()
            
            station_managers = User.objects.filter(
            employee__position__iexact='station manager',
            branch=matching_queue.branch
            )
            for user in station_managers:
                notifications = notification.objects.create(
                     title="Payment Alert",
                     branch=user.branch,
                     user=user,
                     vehicle = matching_queue.vehicle,
                     message=f"Pay Driver {matching_queue.vehicle.plate_number} - Queue Status: FULL",
                     notification_type="p"
                     )
                notifications.save()
            tk = ticket.objects.get(id=ticket_id)
            payments = payment.objects.create(
                user = matching_queue.vehicle.user ,
                vehicle = matching_queue.vehicle,
                status = 'p',
                branch = matching_queue.branch,
                amount = matching_queue.vehicle.route.route_prize * matching_queue.current_passengers ,
                transaction_id = f'TRX-{datetime.now()}-12324',
                types = 'e',
                remark = 'Driver Payment' , 
                tickets = tk
            )
            payments.save()
        else:
            matching_queue.status = 'BOARDING'
            matching_queue.current_passengers = pas
            matching_queue.save()

        # Get related payment
        related_payment = payment.objects.filter(tickets=user_ticket).first()

        # Create travel history
        travel = travelhistory.objects.create(
            branch=matching_queue.branch,
            payment=related_payment,
            ticket=user_ticket,
            vehicle=matching_queue.vehicle,
            used=True,
            user=user
        )
        nid = user.nid
        try:
                t = ticket.objects.get(id=ticket_id)
                t.used = True
                t.save()
                
        except ticket.DoesNotExist:
                return Response({"error": "Ticket not found."}, status=status.HTTP_404_NOT_FOUND)
        
        
        return Response({
            "message": "Passenger boarded",
            "status": matching_queue.status,
            "current_passengers": matching_queue.current_passengers,
            "travel_id": travel.id,
            'ticket_number': ticket_id,
            'first_name': nid.Fname,
            'last_name': nid.Lname,
            'image_url': nid.picture.url if nid.picture else '',
        }, status=status.HTTP_200_OK)

class UserNotificationsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id):
        notifications = notification.objects.filter(user_id=user_id, read=False, notification_type = 'p')
        data = [{"id": n.id, "message": n.message} for n in notifications]
        return Response(data)
    
class UpdateLocationView(generics.CreateAPIView):
    serializer_class = LocationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        latitude = data['latitude']
        longitude = data['longitude']

        user = request.user  # Get user from the token

        assigned_vehicle = vehicle.objects.filter(user=user).first()
        if not assigned_vehicle:
            return Response({'error': 'No vehicle assigned to this user.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the vehicle has tracking enabled
        if not assigned_vehicle.tracking:
            return Response({'error': 'Tracking is disabled for this vehicle.'}, status=status.HTTP_403_FORBIDDEN)

        if assigned_vehicle.location:
            location = assigned_vehicle.location
            location.latitude = latitude
            location.longitude = longitude
            location.tracking = True
            location.save()
        else:
            # Create new location and link it
            location = locations.objects.create(
                latitude=latitude,
                longitude=longitude,
                tracking=True
            )
            assigned_vehicle.location = location
            assigned_vehicle.save()

        return Response({'status': 'Location processed successfully'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def toggle_tracking(request):
    tracking_state = request.data.get('tracking')  # should be True or False

    try:
        # You can choose to update all or a specific row (latest)
        latest = locations.objects.last()
        if latest:
            latest.tracking = tracking_state
            latest.save()
            return Response({'status': f'Tracking set to {tracking_state}'})
        return Response({'error': 'No location record to update'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def toggle_branch_status(request, pk):
    try:
        branch = Branch.objects.get(pk=pk)
        current_status = branch.status
        
        # Define the status rotation
        status_rotation = {
            'a': 'm',  # Active -> Maintenance
            'm': 'i',  # Maintenance -> Inactive
            'i': 'a'   # Inactive -> Active
        }
        
        # Update the status
        branch.status = status_rotation[current_status]
        branch.save()
        
        return Response({
            "status": "success",
            "message": f"Branch status updated to {branch.get_status_display()}",
            "new_status": branch.status,
            "display_status": branch.get_status_display()
        })
    except Branch.DoesNotExist:
        return Response({"error": "Branch not found"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=400)
