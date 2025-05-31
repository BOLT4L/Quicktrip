from user.models import *
from booking.models import *
from rest_framework import serializers
from alert.models import notification ,message
from payment.models import payment
from vehicle_management.models import *
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import nidUser
from datetime import date, datetime
import sys
sys.path.append("..")

User = get_user_model()

class PasswordChangeSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    
    class Meta:
        model = User
        fields = ['old_password', 'new_password']
        extra_kwargs = {
            'old_password': {'write_only': True},
            'new_password': {'write_only': True}
        }
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value
    
    def validate_new_password(self, value):
        validate_password(value)
        return value
    
    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance
class nidSerializer(serializers.ModelSerializer):
    class Meta :
        model = nidUser
        fields = "__all__"
class locationSerializer(serializers.ModelSerializer):
    class Meta:
        model = locations
        fields = "__all__"

class employeSerializer(serializers.ModelSerializer):
    class Meta:
        model = employeeDetail
        fields = "__all__"


class levelSerializer(serializers.ModelSerializer):
    class Meta:
        model = type
        fields = "__all__"

class addtraveller(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ['id','user_type','phone_number','date_joined','branch','nid']

class branchSerializer(serializers.ModelSerializer):
    location = locationSerializer(required = False)
    
    class Meta :
        model = branch
        fields = ['id','location','address','type','name','status']
    
    def create(self, validated_data):
        location_data = validated_data.pop('location')
        branchs = branch.objects.create(
              **validated_data
        )
        
        if location_data:
            loc =locations.objects.create(**location_data)
            branchs.location = loc
            branchs.save()
      
        
        
        return branchs
    

class credSerializer(serializers.ModelSerializer):

    class Meta :
        model = credentials
        fields = ['expiry_date','type','did','doc']
        
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        cred = credentials.objects.create(**validated_data)
   
        if user_data:
             users = user.objects.create(**user_data)
             cred.user = users  # Assign via the OneToOneField
             cred.save()
    
        return cred
    
       
class userSerializer(serializers.ModelSerializer):
    employee = employeSerializer(required=False)
    location = locationSerializer( required=False)
    credentials = credSerializer(required=False)
    branch = branchSerializer(required = False)
    class Meta:
        model = User
        fields = ['id', 'user_type','is_active', 'nid', 'location', 'phone_number','date_joined', 'branch', 'employee', 'credentials']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'branch': {'required': False},
            'location': {'required': False},
            'employee': {'required': False},
            'credentials': {'required': False}
        }
        
    def create(self, validated_data):
        employee_data = validated_data.pop('employee', None)
        credentials_data = validated_data.pop('credentials', None)
        password = validated_data.pop('password', None)
              
        # Create user
        user = User.objects.create(
           
            **validated_data
        )
        
        # Set password if provided
        if password:
            user.set_password(password)
            user.save()
        
        # Create employee if data provided
        if employee_data:
            employee = employeeDetail.objects.create(**employee_data)
            user.employee = employee
            user.save()
        if  credentials_data:
            credential = credentials.objects.create(**credentials_data)
            user.credentials = credential
            user.save()
        
        return user

class ExitSlipSerializer(serializers.ModelSerializer):
    vehicle_plate = serializers.CharField(source='vehicle.plate_number')
    vehicle_model = serializers.CharField(source='vehicle.Model')
    driver_name = serializers.CharField(source='driver.employee.Fname')
    from_location = serializers.CharField(source='from_location.name')
    to_location = serializers.CharField(source='to_location.name')

    class Meta:
        model = ExitSlip
        fields = '__all__'

class VehicleExitSlipSerializer(serializers.ModelSerializer):
    class Meta:
        model = vehicle
        fields = ['plate_number', 'Model', 'color', 'sit_number']
class UserSerializer(serializers.ModelSerializer):
    employee = employeSerializer(required=False)
    branch = branchSerializer(required=False)
    nid = nidSerializer(read_only=True)
    location = locationSerializer(read_only=True)
   
    
    class Meta:
        model = user
        fields = ['id', 'user_type', 'phone_number', 'date_joined', 'branch', 'employee', 'nid', 'location']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
        }
    
    def update(self, instance, validated_data):
        # Handle nested employee updates
        employee_data = validated_data.pop('employee', None)
        if employee_data is not None:
            employee_serializer = self.fields['employee']
            employee_instance = instance.employee
            employee_serializer.update(employee_instance, employee_data)
        
        # Handle nested branch updates
        branch_data = validated_data.pop('branch', None)
        if branch_data is not None:
            branch_serializer = self.fields['branch']
            branch_instance = instance.branch
            branch_serializer.update(branch_instance, branch_data)
        
        # Update regular fields
        return super().update(instance, validated_data)

    
class MessageSerializer(serializers.ModelSerializer):
    sender = userSerializer()
    receiver = userSerializer()

    class Meta:
        model = message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp', 'read']

    def get_sender(self, obj):
        return {
            'id': obj.sender.id,
            'name': f"{obj.sender.employee.Fname} {obj.sender.employee.Lname}",
          
        }

    def get_receiver(self, obj):
        return {
            'id': obj.receiver.id,
            'name': f"{obj.receiver.employee.Fname} {obj.receiver.employee.Lname}",
            
        }
class MessageaddSerializer(serializers.ModelSerializer):
    class Meta:
        model = message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp', 'read']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp', 'read']
        read_only_fields = ['id', 'sender', 'receiver', 'content', 'timestamp']
    
    
  

class routeSerializer(serializers.ModelSerializer):
    first_destination = branchSerializer()
    last_destination = branchSerializer()
    class Meta:
        model = route
        fields = ['id','name','first_destination','last_destination','route_prize','distance']
class routeSerializers(serializers.ModelSerializer):
     class Meta:
        model = route
        fields = ['id','name','first_destination','last_destination','route_prize','distance']
class vehicleSerializer(serializers.ModelSerializer):
    """
    Serializer for vehicle model with proper validation.
    """
    class Meta:
        model = vehicle
        fields = ['route', 'branch', 'year', 'insurance_doc', 'insurance_date', 'name', 'plate_number', 'color', 'Model', 'sit_number', 'picture', 'is_active', 'user', 'types', 'last_updated']
        extra_kwargs = {
            'name': {'required': True},
            'plate_number': {'required': True},
            'color': {'required': True},
            'Model': {'required': True},
            'sit_number': {'required': True},
            'types': {'required': True},
            'user': {'required': True},
            'picture': {'required': True},
            'insurance_doc': {'required': True},
            'insurance_date': {'required': True},
            'branch': {'required': True},
            'route': {'required': False},
            'is_active': {'required': False, 'default': False},
            'last_updated': {'read_only': True}
        }

    def validate_plate_number(self, value):
        """
        Validate that the plate number is unique.
        """
        if vehicle.objects.filter(plate_number=value).exists():
            raise serializers.ValidationError("A vehicle with this plate number already exists.")
        return value

    def validate_sit_number(self, value):
        """
        Validate that the seat number is positive.
        """
        if value <= 0:
            raise serializers.ValidationError("Seat number must be positive.")
        return value

    def validate_insurance_date(self, value):
        """
        Validate that the insurance date is in the future.
        """
        if value < date.today():
            raise serializers.ValidationError("Insurance date must be in the future.")
        return value

class vehiclesSerializer(serializers.ModelSerializer):
    user = userSerializer()
    branch = branchSerializer() 
    types = levelSerializer()
    location = locationSerializer()
    route = routeSerializer()
    class Meta : 
        model = vehicle
        fields =  ['route','branch','year','insurance_doc','insurance_date','name','plate_number','color','Model','sit_number','picture','is_active','user','types','location','last_updated']
class TokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user) 
        token['role'] = user.user_type  
        token['user_id'] = user.id
        if hasattr(user, 'branch') and user.branch:
            token['branch'] = user.branch.id
        else:
            token['branch'] = None
        return token
class ticketSerializer(serializers.ModelSerializer):
    route = routeSerializer()
    level = levelSerializer()
    user = userSerializer()
    class Meta :
        model = ticket
        fields =  ['id','bought_date','route','level','Quantity','takeoff_time','takeoff_date','total_prize','user',]
class buyticketSerializer(serializers.ModelSerializer):
    
    class Meta :
        model = ticket
        fields =  ['id','bought_date','route','level','Quantity','takeoff_time','takeoff_date','total_prize','user',]

   
class paymentSerializer(serializers.ModelSerializer):
    user = userSerializer()
    vehicle = vehicleSerializer(required = False)
    class Meta :
        model = payment
        fields =['id','user','status','branch','date','time','amount','transaction_id','types','remark','vehicle']
  
class addpaymentSerializer(serializers.ModelSerializer):
    class Meta :
        model = payment
        fields =['id','user','status','branch','date','time','amount','transaction_id','types','remark','vehicle']
        extra_kwargs = {
            'vehicle': {'required': False},
            'amount' :{'required': False},
            'remark' :{'required': False},
            'transaction_id' :{'required': False},
             'user' : {'required': False},
                     }
class travelhistorySerializer(serializers.ModelSerializer):
    ticket = ticketSerializer()
    vehicle = vehiclesSerializer()
    payment = paymentSerializer()
 
    class Meta :
        model = travelhistory
        fields = ['id','branch','time','used','ticket','vehicle','payment','user']

class notificationSerilalizer(serializers.ModelSerializer):
    branch = branchSerializer(required = False)
    user = userSerializer(required = False)
    class Meta :
        model = notification
        fields =['id','title','branch','user','message','types','read','time','date']
        extra_kwargs = {
            'message': {'required': False},
        }
 
class UsertravelSerializer(serializers.ModelSerializer):
    travel_history = travelhistorySerializer(
        many=True, 
        read_only=True,
        source='travel_history.all' 
    )
    nid = nidSerializer()
    
    class Meta :
        model = user
        fields = ['id','date_joined','employee','phone_number','nid','travel_history']