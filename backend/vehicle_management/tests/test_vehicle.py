import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from vehicle_management.models import vehicle, type, location
from user.models import user, employeeDetail, branch
import factory
from datetime import date
from django.core.files.uploadedfile import SimpleUploadedFile

class BranchFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = branch

    name = factory.Sequence(lambda n: f'Branch {n}')
    address = factory.Sequence(lambda n: f'Address {n}')
    type = 'b'  # branch type
    status = 'a'  # active

class LocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = location

    longitude = 38.7578
    latitude = 9.0273

class EmployeeDetailFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = employeeDetail

    Fname = factory.Sequence(lambda n: f'Driver{n}')
    Lname = factory.Sequence(lambda n: f'Test{n}')
    position = 'Driver'
    address = 'Test Address'
    Emergency_contact = '123456789'
    Emergency_contact_name = 'Emergency Contact'
    Work_experience = '5 years'

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = user

    phone_number = factory.Sequence(lambda n: int(f'12345{n:04d}'))
    password = factory.PostGenerationMethodCall('set_password', 'testpass123')
    user_type = 'a'  # admin for full access
    is_active = True
    employee = factory.SubFactory(EmployeeDetailFactory)
    branch = factory.SubFactory(BranchFactory)

class VehicleTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = type
    
    level = 'one'  # level one
    detail = 'Standard vehicle type'
    prize = 100.00

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_user():
    return UserFactory()

@pytest.fixture
def driver_user():
    return UserFactory(user_type='d')  # driver type

@pytest.fixture
def vehicle_type():
    return VehicleTypeFactory()

@pytest.fixture
def test_location():
    return LocationFactory()

@pytest.mark.django_db
class TestVehicleAPI:
    def test_create_vehicle(self, api_client, admin_user, driver_user, vehicle_type):
        """Test creating a new vehicle."""
        api_client.force_authenticate(user=admin_user)
        url = reverse('vehicle add', kwargs={'bid': admin_user.branch.id})  # Updated to match URL name in urls.py
        
        # Create test image files
        image_content = b'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
        picture = SimpleUploadedFile('test_picture.gif', image_content, content_type='image/gif')
        insurance_doc = SimpleUploadedFile('test_insurance.gif', image_content, content_type='image/gif')
        
        data = {
            'user': driver_user.id,
            'name': 'Toyota Camry',
            'plate_number': 'ABC123',
            'Model': '2023',
            'year': '2023',
            'color': '#000000',
            'sit_number': 4,
            'types': vehicle_type.id,
            'insurance_date': '2024-12-31',
            'branch': admin_user.branch.id,
            'is_active': False,
            'picture': picture,
            'insurance_doc': insurance_doc
        }
        
        response = api_client.post(url, data, format='multipart')
        assert response.status_code == status.HTTP_201_CREATED
        assert vehicle.objects.count() == 1
        created_vehicle = vehicle.objects.get()
        assert created_vehicle.name == 'Toyota Camry'
        assert created_vehicle.picture
        assert created_vehicle.insurance_doc

    def test_list_vehicles(self, api_client, admin_user):
        """Test retrieving list of vehicles."""
        api_client.force_authenticate(user=admin_user)
        url = reverse('vehicle', kwargs={'did': admin_user.id})  # Updated to match URL name in urls.py
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_get_vehicle_detail(self, api_client, admin_user, driver_user, vehicle_type):
        """Test retrieving a specific vehicle."""
        api_client.force_authenticate(user=admin_user)
        
        # Create test image files
        image_content = b'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
        picture = SimpleUploadedFile('test_picture.gif', image_content, content_type='image/gif')
        insurance_doc = SimpleUploadedFile('test_insurance.gif', image_content, content_type='image/gif')
        
        test_vehicle = vehicle.objects.create(
            user=driver_user,
            name='Honda Civic',
            plate_number='XYZ789',
            Model='2023',
            year='2023',
            color='#FFFFFF',
            sit_number=4,
            types=vehicle_type,
            insurance_date='2024-12-31',
            branch=admin_user.branch,
            is_active=False,
            picture=picture,
            insurance_doc=insurance_doc
        )
        
        url = reverse('location', kwargs={'pk': test_vehicle.pk})  # URL name is correct
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Honda Civic'

    def test_update_vehicle(self, api_client, admin_user, driver_user, vehicle_type):
        """Test updating a vehicle."""
        api_client.force_authenticate(user=admin_user)
        
        # Create test image files
        image_content = b'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
        picture = SimpleUploadedFile('test_picture.gif', image_content, content_type='image/gif')
        insurance_doc = SimpleUploadedFile('test_insurance.gif', image_content, content_type='image/gif')
        
        test_vehicle = vehicle.objects.create(
            user=driver_user,
            name='Honda Civic',
            plate_number='XYZ789',
            Model='2023',
            year='2023',
            color='#FFFFFF',
            sit_number=4,
            types=vehicle_type,
            insurance_date='2024-12-31',
            branch=admin_user.branch,
            is_active=False,
            picture=picture,
            insurance_doc=insurance_doc
        )
        
        url = reverse('location', kwargs={'pk': test_vehicle.pk})  # URL name is correct
        update_data = {
            'name': 'Honda Accord',
            'color': '#000000'
        }
        response = api_client.patch(url, update_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        test_vehicle.refresh_from_db()
        assert test_vehicle.name == 'Honda Accord'
        assert test_vehicle.color == '#000000' 