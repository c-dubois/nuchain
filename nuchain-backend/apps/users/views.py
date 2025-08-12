from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from .serializers import (
    UserRegistrationSerializer,
    UserProfileSerializer,
    CustomTokenObtainPairSerializer,
    UserUpdateSerializer
)

class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom JWT login view that returns user info along with tokens"""
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            username = request.data.get('username')
            try:
                user = User.objects.get(username=username)

                response.data.update({
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'balance': float(user.profile.balance)
                    },
                    'message': 'Login successful!'
                })
            except User.DoesNotExist:
                pass
        
        return response
    
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    """Register a new user and return JWT tokens"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        access_token['username'] = user.username
        access_token['email'] = user.email

        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'balance': float(user.profile.balance)
            },
            'refresh': str(refresh),
            'access': str(access_token),
            'message': 'User created successfully with 25,000 $NUC tokens!'
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_profile(request):
    """Get current user's profile including balance"""
    serializer = UserProfileSerializer(request.user.profile)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_user_profile(request):
    """Update user's profile information"""
    serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        profile_serializer = UserProfileSerializer(request.user.profile)
        return Response({
            'user': profile_serializer.data,
            'message': 'Profile updated successfully'
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_password(request):
    """Change user's password"""
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    
    if not request.user.check_password(old_password):
        return Response({'error': 'Current password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
    
    request.user.set_password(new_password)
    request.user.save()
    
    return Response({'message': 'Password changed successfully'})

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def reset_wallet(request):
    """Reset user's wallet to starting balance (25,000 $NUC) and clear investments"""

    request.user.profile.reset_wallet()
    
    return Response({
        'message': 'Wallet reset successfully! Your balance is now 25,000 $NUC.',
        'balance': float(request.user.profile.balance)
    })

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_user(request):
    """Logout user by blacklisting refresh token"""
    try:
        refresh_token = request.data.get("refresh")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Refresh token required'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': f'Error logging out: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_account(request):
    """Delete user's account"""
    try:
        request.user.delete()
        return Response({'message': 'Account deleted successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': f'Failed to delete account: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)