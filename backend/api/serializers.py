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
import sys
import json
from backend.config import send_twilio_message

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
        model = User
        fields = ['id','user_type','phone_number','date_joined','branch','nid']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = locations
        fields = ['latitude', 'longitude']

class branchSerializer(serializers.ModelSerializer):
    location = LocationSerializer(required=False)
    
    class Meta:
        model = Branch
        fields = ['id', 'location', 'address', 'type', 'name', 'status']
    
    def create(self, validated_data):
        # Safely extract location data (returns None if not provided)
        location_data = validated_data.pop('location', None)
        
        # Create branch instance without location first
        branch = Branch.objects.create(**validated_data)
        
        # Handle location if provided
        if location_data:
            # Check if we're referencing an existing location
            if 'id' in location_data:
                try:
                    location = locations.objects.get(id=location_data['id'])
                    branch.location = location
                    
                except locations.DoesNotExist:
                    raise serializers.ValidationError(
                        {'location': 'Referenced location does not exist'}
                    )
            else:
                # Create new location instance
                location = locations.objects.create(**location_data)
                branch.location = location
            
            branch.save()
            notifications = notification.objects.create( title = "Branch Created",branch = branch ,message = f"Branch {branch.name} has been created", notification_type = "a")
            notifications.save()
        return branch

    def update(self, instance, validated_data):
        location_data = validated_data.pop('location', None)
        
        # Update regular fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Handle location update
        if location_data is not None:
            if instance.location:
                # Update existing location
                if 'id' in location_data:
                    # Verify the ID matches if provided
                    if location_data['id'] != instance.location.id:
                        raise serializers.ValidationError(
                            {'location': 'Cannot change location ID'}
                        )
                    # Update other fields
                    for attr, value in location_data.items():
                        if attr != 'id':
                            setattr(instance.location, attr, value)
                    instance.location.save()
                else:
                    # Update fields without changing ID
                    for attr, value in location_data.items():
                        setattr(instance.location, attr, value)
                    instance.location.save()
            else:
                # Create new location if none exists
                if 'id' in location_data:
                    try:
                        instance.location = locations.objects.get(id=location_data['id'])
                    except locations.DoesNotExist:
                        raise serializers.ValidationError(
                            {'location': 'Referenced location does not exist'}
                        )
                else:
                    instance.location = locations.objects.create(**location_data)
        
        instance.save()
        return instance

class credSerializer(serializers.ModelSerializer):

    class Meta :
        model = credentials
        fields = ['expiry_date','type','did','doc']
        
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        cred = credentials.objects.create(**validated_data)
   
        if user_data:
             users = User.objects.create(**user_data)
             cred.user = users  # Assign via the OneToOneField
             cred.save()
    
        return cred
class adddriverSerializer(serializers.ModelSerializer):
    employee = employeSerializer(required=False)
    location = LocationSerializer(required=False)
    credentials = credSerializer(required=False)
    
    branch = serializers.CharField(write_only=True, required=False)  # Accept JSON string here
    
    class Meta:
        model = User
        fields = [
            'id', 'user_type', 'is_active', 'nid', 'location',
            'phone_number', 'date_joined', 'branch', 'employee', 'credentials', 'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
        }

    def validate_branch(self, value):
        """Parse JSON string and validate branch dict"""
        if not value:
            return None
        
        try:
            branch_data = json.loads(value)
        except json.JSONDecodeError:
            raise serializers.ValidationError("Branch must be a valid JSON string")
        
        if not isinstance(branch_data, dict):
            raise serializers.ValidationError("Branch must be a JSON object")
        
        branch_id = branch_data.get('id')
        if not branch_id:
            raise serializers.ValidationError("Branch ID is required inside the branch object")
        
        if not Branch.objects.filter(id=branch_id).exists():
            raise serializers.ValidationError("Branch with this ID does not exist")
        
        return branch_data

    def create(self, validated_data):
        employee_data = validated_data.pop('employee', None)
        credentials_data = validated_data.pop('credentials', None)
        location_data = validated_data.pop('location', None)
        branch_data = validated_data.pop('branch', None)
        password = validated_data.pop('password', None)
        
        # branch_data here is a dict, from validate_branch
        try:
            user = User.objects.create(**validated_data)
            if password:
                user.set_password(password)

            if branch_data and branch_data.get('id'):
                user.branch_id = branch_data['id']

            if employee_data:
                user.employee = employeeDetail.objects.create(**employee_data)
            if credentials_data:
                user.credentials = credentials.objects.create(**credentials_data)
            if location_data:
                user.location = locations.objects.create(**location_data)

            user.save()
            return user

        except Exception as e:
            if 'user' in locals():
                user.delete()
            raise serializers.ValidationError(f"Failed to create user: {str(e)}")

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.branch:
            rep['branch'] = branchSerializer(instance.branch).data
        return rep
class userSerializer(serializers.ModelSerializer):
    employee = employeSerializer(required=False)
    location = LocationSerializer(required=False)
    credentials = credSerializer(required=False)
    
    # Change to DictField to handle the nested structure
    branch = serializers.DictField(required=False, write_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'user_type', 'is_active', 'nid', 'location',
            'phone_number', 'date_joined', 'branch', 'employee', 'credentials'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
        }

    def validate_branch(self, value):
        """Custom validation for branch field"""
        if value is None:
            return None
            
        if not isinstance(value, dict):
            raise serializers.ValidationError("Branch must be an object")
            
        branch_id = value.get('id')
        if not branch_id:
            raise serializers.ValidationError("Branch ID is required")
            
        try:
            Branch.objects.get(id=branch_id)
        except Branch.DoesNotExist:
            raise serializers.ValidationError("Branch with this ID does not exist")
            
        return value

    def create(self, validated_data):
        # Extract nested data
        employee_data = validated_data.pop('employee', None)
        credentials_data = validated_data.pop('credentials', None)
        location_data = validated_data.pop('location', None)
        branch_data = validated_data.pop('branch', None)
        password = validated_data.pop('password', None)
        
        try:
            # Create user first
            user = User.objects.create(**validated_data)
            
            if password:
                user.set_password(password)

            # Handle branch assignment
            if branch_data and branch_data.get('id'):
                user.branch_id = branch_data['id']

            # Handle other relations
            if employee_data:
                user.employee = employeeDetail.objects.create(**employee_data)
            if credentials_data:
                user.credentials = credentials.objects.create(**credentials_data)
            if location_data:
                user.location = locations.objects.create(**location_data)

            user.save()
            return user

        except Exception as e:
            if 'user' in locals():
                user.delete()
            raise serializers.ValidationError(f"Failed to create user: {str(e)}")

    def to_representation(self, instance):
        """Convert branch ID to full branch object in response"""
        representation = super().to_representation(instance)
        if instance.branch:
            representation['branch'] = branchSerializer(instance.branch).data
        return representation
class EmployeeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = employeeDetail
        fields = ['id', 'Fname', 'Lname', 'position']
class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id', 'name', 'address']      

class OTPSerializer(serializers.ModelSerializer):
    class Meta :
        model = OTP
        fields = ['id', 'phone_number']

class QueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queues
        fields = '__all__'
        read_only_fields = ['date', 'time', 'position', 'status']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = notification
        fields = '__all__'
        read_only_fields = ('time', 'date', 'read')

class VehicleLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = vehicle
        fields = ['id', 'plate_number', 'location']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'phone_number', 'password', 'user_type']
        extra_kwargs = {
            'password': {'write_only': True},
            'user_type': {'default': 'u'}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            phone_number=validated_data['phone_number'],
            password=validated_data['password'],
            user_type=validated_data.get('user_type', 'u'),
          
        )
        return user
class UserSerializers(serializers.ModelSerializer):
    employee = EmployeeDetailSerializer()
    
    class Meta:
        model = User
        fields = ['id', 'user_type', 'phone_number', 'branch', 'employee']
        
    def update(self, instance, validated_data):
        # Update branch
        instance.branch = validated_data.get('branch', instance.branch)
        instance.save()
        
        # Update employee position if provided
        employee_data = validated_data.pop('employee', {})
        if employee_data and hasattr(instance, 'employee'):
            employee = instance.employee
            employee.position = employee_data.get('position', employee.position)
            employee.save()
            
        return instance   
class usersSerializer(serializers.ModelSerializer):
    employee = employeSerializer(required=False)
    location = LocationSerializer(required=False)
    credentials = credSerializer(required=False)
    
    # Change to DictField to handle the nested structure
    branch = serializers.DictField(required=False, write_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'user_type', 'is_active', 'nid', 'location',
            'phone_number', 'date_joined', 'branch', 'employee', 'credentials','password'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_branch(self, value):
        """Custom validation for branch field"""
        if value is None:
            return None
            
        if not isinstance(value, dict):
            raise serializers.ValidationError("Branch must be an object")
            
        branch_id = value.get('id')
        if not branch_id:
            raise serializers.ValidationError("Branch ID is required")
            
        try:
            Branch.objects.get(id=branch_id)
        except Branch.DoesNotExist:
            raise serializers.ValidationError("Branch with this ID does not exist")
            
        return value

    def create(self, validated_data):
        # Extract nested data
        employee_data = validated_data.pop('employee', None)
        credentials_data = validated_data.pop('credentials', None)
        location_data = validated_data.pop('location', None)
        branch_data = validated_data.pop('branch', None)
        password = validated_data.pop('password', None)
        
        try:
            # Create user first
            user = User.objects.create(**validated_data)
            
            if password:
                user.set_password(password)

            # Handle branch assignment
            if branch_data and branch_data.get('id'):
                user.branch_id = branch_data['id']

            # Handle other relations
            if employee_data:
                user.employee = employeeDetail.objects.create(**employee_data)
            if credentials_data:
                user.credentials = credentials.objects.create(**credentials_data)
            if location_data:
                user.location = locations.objects.create(**location_data)
            notifications = notification.objects.create( title = "Subadmin Registered",branch = user.branch ,user =user,message = f"Sub admin {employee_data['Fname']} {employee_data['Lname']} has been Registerd as {employee_data['position']}", notification_type = "a")
            notifications.save()
            user.save()
            try:
                message_body = f"""
                QUICKTRIP OTP

                Hello,

                Your Current Password is: {password}

                Please Change Password after Login
                """
                send_twilio_message(user.phone_number if user.phone_number.startswith('+') else f'+{user.phone_number}', message_body)

            except Exception as e:
                print(f"Error sending Message: {e}")
            
            return user

        except Exception as e:
            if 'user' in locals():
                user.delete()
            raise serializers.ValidationError(f"Failed to create user: {str(e)}")

    def to_representation(self, instance):
        """Convert branch ID to full branch object in response"""
        representation = super().to_representation(instance)
        if instance.branch:
            representation['branch'] = branchSerializer(instance.branch).data
        return representation
    

class QueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queues
        fields = '__all__'
class VehicleExitSlipSerializer(serializers.ModelSerializer):
    class Meta:
        model = vehicle
        fields = ['plate_number', 'Model', 'color', 'sit_number']
class ExitSlipSerializer(serializers.ModelSerializer):
    from_location = serializers.CharField(source='from_location.name')
    to_location = serializers.CharField(source='to_location.name')
    vehicle = VehicleExitSlipSerializer(required = False)
    class Meta:
        model = ExitSlip
        fields = '__all__'
class LocationUpdateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    
class UserSerializer(serializers.ModelSerializer):
    employee = employeSerializer(required=False)
    branch = branchSerializer(required=False)
    nid = nidSerializer(read_only=True)
    location = LocationSerializer(read_only=True)
   
    
    class Meta:
        model = User
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
     def create(self, validated_data):
        
        routes = route.objects.create(**validated_data)
        routes.save()
        notifications = notification.objects.create( title = "Route Created",user = self.context['request'].user ,branch = validated_data.pop('first_destination') ,message = f"Route {validated_data.pop('name')} has been created", notification_type = "a")
        notifications.save()
        return routes


class vehicleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = vehicle
        fields =  ['id','route','branch','year','insurance_doc','insurance_date','name','plate_number','color','Model','sit_number','picture','is_active','user','types','last_updated','long','detail','payment_rate','tracking']

class vehiclesSerializer(serializers.ModelSerializer):
    user = userSerializer()
    branch = branchSerializer() 
    types = levelSerializer()
    location = LocationSerializer()
    route = routeSerializer()
    class Meta : 
        model = vehicle
        fields =  ['payment_rate','long','detail','id','route','branch','year','insurance_doc','insurance_date','name','plate_number','color','Model','sit_number','picture','is_active','user','types','location','last_updated','tracking']
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
        fields =  ['id','bought_date','route','level','Quantity','takeoff_time','takeoff_date','total_prize','user','ticket_type']

   
class paymentSerializer(serializers.ModelSerializer):
    user = userSerializer()
    vehicle = vehicleSerializer(required = False)
    class Meta :
        model = payment
        fields =['id','user','status','branch','date','time','amount','transaction_id','types','remark','vehicle']
  
class addpaymentSerializer(serializers.ModelSerializer):
    class Meta :
        model = payment
        fields =['id','user','status','branch','date','time','amount','transaction_id','types','remark','vehicle','tickets',]
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
        fields =['id','title','branch','user','message','notification_type','read','time','date']
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
        model = User
        fields = ['id','date_joined','employee','phone_number','nid','travel_history']


class NotificationSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%B %d, %Y")
    time = serializers.TimeField(format="%I:%M %p")
    branch = branchSerializer()
    
    class Meta:
        model = notification
        fields = ['id', 'title', 'message', 'date', 'time', 'read', 
                 'notification_type', 'branch', 'vehicle']


class leaveToQueueSerializer(serializers.Serializer):
    vehicle_id = serializers.IntegerField()
class AddToQueueSerializer(serializers.Serializer):
    branch_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
class VehicleLocationSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(source='location.latitude')
    longitude = serializers.FloatField(source='location.longitude')

    class Meta:
        model = vehicle
        fields = ['id', 'name','tracking', 'plate_number', 'color', 'latitude', 'longitude', 'last_updated']

class BoardingSerializer(serializers.Serializer):
    ticket_id = serializers.IntegerField()

class RetrieveQueueSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.name', default="")
    destination_name = serializers.CharField(source='dest.name', default="")
    vehicle = serializers.CharField(source='vehicle.plate_number', default="")  
    level = serializers.CharField(source='level.name', default="")  


    class Meta:
        model = Queues
        fields = [
            'branch_name',
            'destination_name',
            'position',
            'level',
            'vehicle',
            'current_passengers',
            'status',
            'date',
            'time',
        ]
