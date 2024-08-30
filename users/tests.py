from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import User
from .serializers import UserRegisterSerializer

class UserModelTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.User = get_user_model()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'securepassword123',
            'password2': 'securepassword123',
            'first_name': 'Test',
            'last_name': 'User',
            'role': 'Admin'  
        }

    def test_create_user(self):
        serializer = UserRegisterSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.username, self.user_data['username'])
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.check_password(self.user_data['password']))

    def test_user_creation_invalid_email(self):
        invalid_user_data = self.user_data.copy()
        invalid_user_data['email'] = 'invalid_email'
        serializer = UserRegisterSerializer(data=invalid_user_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_user_creation_password_mismatch(self):
        invalid_user_data = self.user_data.copy()
        invalid_user_data['password2'] = 'differentpassword'
        serializer = UserRegisterSerializer(data=invalid_user_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_user_login(self):
        user = self.User.objects.create_user(
            username=self.user_data['username'],
            email=self.user_data['email'],
            password=self.user_data['password']
        )
        
        response = self.client.post('/users/login/', {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data) 

    def test_user_login_invalid_credentials(self):
        response = self.client.post('/users/login/', {
            'username': 'nonexistentuser',
            'password': 'wrongpassword'
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_endpoint(self):
        response = self.client.post('/users/register/', self.user_data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username=self.user_data['username']).exists())

    # def test_get_user_profile(self):
    #     user = self.User.objects.create_user(**self.user_data)
    #     self.client.force_authenticate(user=user)
        
    #     response = self.client.get('/users/profile/')
        
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['username'], self.user_data['username'])
    #     self.assertEqual(response.data['email'], self.user_data['email'])