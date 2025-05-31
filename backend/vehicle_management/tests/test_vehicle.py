import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from vehicle_management.models import vehicle, type, location
from user.models import user, employeeDetail, branch
import factory
from datetime import date
from django.core.files.uploadedfile import SimpleUploadedFile
import shutil
import os
from django.conf import settings

class BranchFactory(factory.django.DjangoModelFactory):
    """Factory for creating test Branch instances."""
    class Meta:
        model = branch
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: f'Branch {n}')
    address = factory.Sequence(lambda n: f'Address {n}')
    type = 'b'  # branch type
    status = 'a'  # active

class LocationFactory(factory.django.DjangoModelFactory):
    """Factory for creating test Location instances."""
    class Meta:
        model = location
        django_get_or_create = ('longitude', 'latitude')

    longitude = 38.7578
    latitude = 9.0273

class EmployeeDetailFactory(factory.django.DjangoModelFactory):
    """Factory for creating test EmployeeDetail instances."""
    class Meta:
        model = employeeDetail
        django_get_or_create = ('Fname', 'Lname')

    Fname = factory.Sequence(lambda n: f'Driver{n}')
    Lname = factory.Sequence(lambda n: f'Test{n}')
    position = 'Driver'
    address = 'Test Address'
    Emergency_contact = '123456789'
    Emergency_contact_name = 'Emergency Contact'
    Work_experience = '5 years'

class UserFactory(factory.django.DjangoModelFactory):
    """Factory for creating test User instances."""
    class Meta:
        model = user
        django_get_or_create = ('phone_number',)
        skip_postgeneration_save = True

    phone_number = factory.Sequence(lambda n: int(f'12345{n:04d}'))
    password = factory.PostGenerationMethodCall('set_password', 'testpass123')
    user_type = 'a'  # admin for full access
    is_active = True
    employee = factory.SubFactory(EmployeeDetailFactory)
    branch = factory.SubFactory(BranchFactory)

class VehicleTypeFactory(factory.django.DjangoModelFactory):
    """Factory for creating test VehicleType instances."""
    class Meta:
        model = type
        django_get_or_create = ('level',)
    
    level = 'one'  # level one
    detail = 'Standard vehicle type'
    prize = 100.00

@pytest.fixture
def api_client():
    """Fixture providing an API client instance."""
    return APIClient()

@pytest.fixture
def admin_user():
    """Fixture providing an admin user instance."""
    return UserFactory()

@pytest.fixture
def driver_user():
    """Fixture providing a driver user instance."""
    return UserFactory(user_type='d')  # driver type

@pytest.fixture
def vehicle_type():
    """Fixture providing a vehicle type instance."""
    return VehicleTypeFactory()

@pytest.fixture
def test_location():
    """Fixture providing a location instance."""
    return LocationFactory()

@pytest.fixture(autouse=True)
def cleanup_media():
    """Fixture to clean up uploaded media files after tests."""
    yield
    if os.path.exists(settings.MEDIA_ROOT):
        shutil.rmtree(settings.MEDIA_ROOT)

@pytest.fixture
def test_image():
    """Fixture providing a test image file."""
    image_content = b'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
    return SimpleUploadedFile('test_image.gif', image_content, content_type='image/gif')

@pytest.mark.django_db
class TestVehicleAPI:
    """Test suite for Vehicle API endpoints."""

    def test_create_vehicle_success(self, api_client, admin_user, driver_user, vehicle_type, test_image):
        """
        Test successful vehicle creation with all required fields.
        Should return 201 Created and create a vehicle instance.
        """
        api_client.force_authenticate(user=admin_user)
        url = reverse('vehicle add', kwargs={'bid': admin_user.branch.id})
        
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
            'picture': test_image,
            'insurance_doc': test_image
        }
        
        response = api_client.post(url, data, format='multipart')
        assert response.status_code == status.HTTP_201_CREATED
        assert vehicle.objects.count() == 1
        
        created_vehicle = vehicle.objects.get()
        assert created_vehicle.name == 'Toyota Camry'
        assert created_vehicle.plate_number == 'ABC123'
        assert created_vehicle.user == driver_user
        assert created_vehicle.branch == admin_user.branch
        assert created_vehicle.picture
        assert created_vehicle.insurance_doc

    def test_create_vehicle_missing_required_fields(self, api_client, admin_user):
        """
        Test vehicle creation with missing required fields.
        Should return 400 Bad Request.
        """
        api_client.force_authenticate(user=admin_user)
        url = reverse('vehicle add', kwargs={'bid': admin_user.branch.id})
        
        data = {
            'name': 'Toyota Camry',  # Missing other required fields
        }
        
        response = api_client.post(url, data, format='multipart')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_list_vehicles(self, api_client, admin_user):
        """
        Test retrieving list of vehicles.
        Should return 200 OK and list of vehicles.
        """
        api_client.force_authenticate(user=admin_user)
        url = reverse('vehicle', kwargs={'did': admin_user.id})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)

    def test_get_vehicle_detail(self, api_client, admin_user, driver_user, vehicle_type, test_image):
        """
        Test retrieving a specific vehicle's details.
        Should return 200 OK and vehicle details.
        """
        api_client.force_authenticate(user=admin_user)
        
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
            picture=test_image,
            insurance_doc=test_image
        )
        
        url = reverse('location', kwargs={'pk': test_vehicle.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Honda Civic'
        assert response.data['plate_number'] == 'XYZ789'
        assert response.data['color'] == '#FFFFFF'

    def test_update_vehicle(self, api_client, admin_user, driver_user, vehicle_type, test_image):
        """
        Test updating a vehicle's information.
        Should return 200 OK and update the vehicle instance.
        """
        api_client.force_authenticate(user=admin_user)
        
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
            picture=test_image,
            insurance_doc=test_image
        )
        
        url = reverse('location', kwargs={'pk': test_vehicle.pk})
        update_data = {
            'name': 'Honda Accord',
            'color': '#000000',
            'sit_number': 5
        }
        response = api_client.patch(url, update_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        
        test_vehicle.refresh_from_db()
        assert test_vehicle.name == 'Honda Accord'
        assert test_vehicle.color == '#000000'
        assert test_vehicle.sit_number == 5

    def test_delete_vehicle(self, api_client, admin_user, driver_user, vehicle_type, test_image):
        """
        Test deleting a vehicle.
        Should return 204 No Content and delete the vehicle instance.
        """
        api_client.force_authenticate(user=admin_user)
        
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
            picture=test_image,
            insurance_doc=test_image
        )
        
        url = reverse('location', kwargs={'pk': test_vehicle.pk})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not vehicle.objects.filter(pk=test_vehicle.pk).exists()

    def test_unauthorized_access(self, api_client, admin_user, driver_user, vehicle_type, test_image):
        """
        Test unauthorized access to vehicle endpoints.
        Should return 401 Unauthorized.
        """
        # Try to create vehicle without authentication
        url = reverse('vehicle add', kwargs={'bid': admin_user.branch.id})
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
            'picture': test_image,
            'insurance_doc': test_image
        }
        response = api_client.post(url, data, format='multipart')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED 