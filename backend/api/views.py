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
from django.http import HttpResponse
from django.db.models import Sum
from datetime import datetime, timedelta
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from io import BytesIO 
from django.contrib.auth import update_session_auth_hash
import sys
sys.path.append("..")
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Transaction

def home(request):
    return render(request, 'home.html')

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
class phone_number_search(generics.ListAPIView):
    serializer_class = nidSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        pn = self.kwargs['pn']
        return nidUser.objects.filter(phone_number = pn)

class Fan_search(generics.ListAPIView):
    serializer_class = nidSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        fan = self.kwargs['fan']
        return nidUser.objects.filter(FAN = fan)
    
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
    
class ExitSlipListCreateView(generics.ListCreateAPIView):
    serializer_class = ExitSlipSerializer

    def get_queryset(self):
        driver_id = self.request.query_params.get('driver')
        return ExitSlip.objects.filter(driver=driver_id).order_by('-departure_time')

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
        
class tickets(generics.ListAPIView):
    serializer_class = ticketSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        users = self.request.user
        if users.user_type == 'a':
            return ticket.objects.all()  
        elif users.user_type == 's' and users.branch:
            return ticket.objects.filter(route__first_destination=users.branch)  
        else:
            return route.objects.none()  
        
class buyticket(generics.CreateAPIView):
    serializer_class = buyticketSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        users = self.request.user
        if users.user_type == 'a':
            return ticket.objects.all()  
        elif users.user_type == 's' and users.branch:
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
            return payment.objects.all()  
        elif users.user_type == 's' and users.branch:
            return payment.objects.filter(branch=users.branch,user__user_type = "d") 
        return  payment.objects.none()  

class vehicles(generics.ListCreateAPIView):
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

class driver_vehicle(generics.ListAPIView):
    serializer_class = vehiclesSerializer
    permission_classes = [IsAuthenticated]
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
    
class payDriver(generics.RetrieveUpdateAPIView):
    queryset = payment.objects.all()
    serializer_class = addpaymentSerializer
    permission_classes = [IsAuthenticated]   
    lookup_field = 'id'

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()       
        instance.status = 'c'
        instance.save()
       
        serializer = self.get_serializer(instance)
        return Response(serializer.data)   
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