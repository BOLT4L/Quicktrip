import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from vehicle_management.models import vehicle, type
from user.models import user
from payment.models import payment
import factory
from datetime import datetime, timedelta

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = user

    username = factory.Sequence(lambda n: f'user{n}')
    password = factory.PostGenerationMethodCall('set_password', 'testpass123')
    email = factory.Sequence(lambda n: f'user{n}@example.com')
    phone_number = factory.Sequence(lambda n: f'123456789{n}')
    user_type = 'a'  # admin

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_user():
    return UserFactory()

@pytest.mark.django_db
class TestVehicleAPI:
    def test_authentication(self, api_client, admin_user):
        """Test user authentication."""
        url = reverse('get_token')  # Your token URL
        data = {
            'username': admin_user.username,
            'password': 'testpass123'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_vehicle_list_endpoint(self, api_client, admin_user):
        """Test vehicle listing endpoint."""
        api_client.force_authenticate(user=admin_user)
        url = reverse('vehicles-list')  # Your vehicles list URL
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)

    def test_payment_creation(self, api_client, admin_user):
        """Test payment creation endpoint."""
        api_client.force_authenticate(user=admin_user)
        url = reverse('payment-create')  # Your payment creation URL
        data = {
            'amount': 1000.00,
            'types': 'i',  # income
            'status': 'c',  # completed
            'transaction_id': 'TEST123',
            'remark': 'Test payment'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert payment.objects.count() == 1
        assert payment.objects.get().amount == 1000.00

    def test_dashboard_stats(self, api_client, admin_user):
        """Test dashboard statistics endpoint."""
        api_client.force_authenticate(user=admin_user)
        url = reverse('dashboard-stats')  # Your dashboard stats URL
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'total_vehicles' in response.data
        assert 'total_revenue' in response.data
        assert 'tax_collected' in response.data 