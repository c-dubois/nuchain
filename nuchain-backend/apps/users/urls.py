from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.get_user_profile, name='user-profile'),
    path('profile/update/', views.update_user_profile, name='update-profile'),
    path('wallet/reset/', views.reset_wallet, name='reset-wallet'),
    path('password/change/', views.change_password, name='change-password'),
    path('account/delete/', views.delete_account, name='delete-account'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]