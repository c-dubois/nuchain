from django.test import TestCase
from django.contrib.auth.models import User
from apps.users.serializers import (
    UserSerializer,
    UserProfileSerializer,
    UserRegistrationSerializer,
    CustomTokenObtainPairSerializer,
    UserUpdateSerializer
)

class UserSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )

    def test_user_serializer_fields(self):
        """Test that UserSerializer returns correct fields"""
        serializer = UserSerializer(instance=self.user)
        data = serializer.data
        
        self.assertEqual(set(data.keys()), {'id', 'username', 'email', 'first_name', 'last_name', 'date_joined'})
        self.assertEqual(data['username'], 'testuser')
        self.assertEqual(data['email'], 'test@example.com')
        self.assertEqual(data['first_name'], 'Test')
        self.assertEqual(data['last_name'], 'User')

class UserProfileSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.profile = self.user.profile
        
    def test_user_profile_serializer_fields(self):
        """Test that UserProfileSerializer returns correct fields"""
        serializer = UserProfileSerializer(instance=self.profile)
        data = serializer.data
        
        self.assertEqual(set(data.keys()), {'id', 'user', 'balance', 'created_at'})
        self.assertEqual(data['user'], self.user.id)
        self.assertEqual(data['balance'], str(self.profile.balance))

class UserRegistrationSerializerTest(TestCase):
    def test_valid_registration_data(self):
        """Test serializer with valid registration data"""
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'strongpass123',
            'password_confirm': 'strongpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        
        serializer = UserRegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
    
    def test_password_mismatch(self):
        """Test serializer with mismatched passwords"""
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'pass12345',
            'password_confirm': 'differentpass'
        }
        
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)
        self.assertIn('Passwords do not match.', serializer.errors['non_field_errors'])
    
    def test_short_password(self):
        """Test serializer with password shorter than 8 characters"""
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'short',
            'password_confirm': 'short'
        }
        
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)
    
    def test_create_user(self):
        """Test user creation through serializer"""
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'strongpass123',
            'password_confirm': 'strongpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        
        serializer = UserRegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        user = serializer.save()
        
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.email, 'new@example.com')
        self.assertTrue(user.check_password('strongpass123'))
        self.assertTrue(hasattr(user, 'profile'))

class CustomTokenObtainPairSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_get_token(self):
        """Test that token contains user info"""
        serializer = CustomTokenObtainPairSerializer.get_token(self.user)
        
        self.assertIn('username', serializer)
        self.assertIn('email', serializer)
        self.assertEqual(serializer['username'], self.user.username)
        self.assertEqual(serializer['email'], self.user.email)

class UserUpdateSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='pass123'
        )
    
    def test_update_user_info(self):
        """Test updating user information"""
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com'
        }
        
        serializer = UserUpdateSerializer(self.user, data=data)
        self.assertTrue(serializer.is_valid())
        
        updated_user = serializer.save()
        self.assertEqual(updated_user.first_name, 'Updated')
        self.assertEqual(updated_user.last_name, 'Name')
        self.assertEqual(updated_user.email, 'updated@example.com')
    
    def test_update_with_existing_email(self):
        """Test updating with email already in use by another user"""
        User.objects.create_user(
            username='other',
            email='taken@example.com',
            password='pass123'
        )
        
        data = {'email': 'taken@example.com'}
        
        serializer = UserUpdateSerializer(self.user, data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)