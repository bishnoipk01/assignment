# myapp/tests.py
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from .models import Company

User = get_user_model()

class OverallAppTestCase(APITestCase):
    def setUp(self):
        # Create two test users
        self.user1 = User.objects.create_user(
            email="user1@example.com", password="pass1234",
            first_name="User1", last_name="One"
        )
        self.user2 = User.objects.create_user(
            email="user2@example.com", password="pass5678",
            first_name="User2", last_name="Two"
        )
        # Create a test company
        self.company = Company.objects.create(
            name="Test Company",
            address="123 Test Street",
            description="A test company."
        )

    def authenticate(self, user):
        """
        Helper method: authenticate a user using token auth.
        """
        token, _ = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_registration_api(self):
        """
        Test that a new user can register via the API.
        """
        url = reverse('api_user_register')
        data = {
            "email": "newuser@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "newpassword123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_user = User.objects.get(email="newuser@example.com")
        self.assertEqual(new_user.first_name, "New")

    def test_token_auth(self):
        """
        Test that a valid token is returned on login.
        Assumes the token endpoint URL name is 'api_token_auth' and expects an 'email' field.
        """
        url = reverse('api_token_auth')
        data = {"email": "user1@example.com", "password": "pass1234"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        
    def test_company_list_api(self):
        """
        Test that an authenticated user can list companies.
        """
        self.authenticate(self.user1)
        url = reverse('api_company_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_company_create_api_admin_only(self):
        """
        Test that only admin users can create a new company.
        For this test, promote user1 to admin.
        """
        self.user1.is_staff = True
        self.user1.save()
        self.authenticate(self.user1)
        url = reverse('api_company_list')
        data = {
            "name": "New Company",
            "address": "456 New Ave",
            "description": "A newly created company."
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "New Company")

    def test_company_update_forbidden_for_normal_user(self):
        """
        Test that a normal user cannot update company details.
        """
        self.authenticate(self.user1)
        url = reverse('api_company_detail', args=[self.company.id])
        data = {"address": "789 Updated Blvd"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_update_own_profile(self):
        """
        Test that a user can update their own profile.
        """
        self.authenticate(self.user1)
        url = reverse('api_user_detail', args=[self.user1.id])
        data = {"first_name": "UpdatedUser1"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.first_name, "UpdatedUser1")

    def test_user_update_other_profile_forbidden(self):
        """
        Test that a normal user cannot update another user's profile.
        """
        self.authenticate(self.user1)
        url = reverse('api_user_detail', args=[self.user2.id])
        data = {"first_name": "HackerName"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_update_other_profile(self):
        """
        Test that an admin user can update another user's profile.
        """
        # Promote user1 to admin
        self.user1.is_staff = True
        self.user1.save()
        self.authenticate(self.user1)
        url = reverse('api_user_detail', args=[self.user2.id])
        data = {"first_name": "AdminUpdated"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user2.refresh_from_db()
        self.assertEqual(self.user2.first_name, "AdminUpdated")
