from django.urls import path
from django.contrib.auth import views as auth_views
from .views import company_detail, user_detail, user_edit, home, register
from .forms import EmailAuthenticationForm
from rest_framework.authtoken.views import obtain_auth_token

from .views_api import (
    CompanyListCreateAPI,
    CompanyRetrieveUpdateDestroyAPI,
    UserListCreateAPI,
    UserRetrieveUpdateDestroyAPIView,
    UserRegistrationAPI,
    CustomObtainAuthToken
)

urlpatterns = [
    # Home page
    path('', home, name='home'),

    # Registration
    path('register/', register, name='register'),

    # Authentication URLs: use our custom login form
    path('login/', auth_views.LoginView.as_view(
            template_name='login.html',
            authentication_form=EmailAuthenticationForm
         ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Detail and edit pages (protected by login)
    path('company/<int:pk>/', company_detail, name='company_detail'),
    path('user/<int:pk>/', user_detail, name='user_detail'),
    path('user/<int:pk>/edit/', user_edit, name='user_edit'),

    # API endpoints for Company
    path('api/companies/', CompanyListCreateAPI.as_view(), name='api_company_list'),
    path('api/companies/<int:pk>/', CompanyRetrieveUpdateDestroyAPI.as_view(), name='api_company_detail'),

    # API endpoints for User
    path('api/users/', UserListCreateAPI.as_view(), name='api_user_list'),
    path('api/users/<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='api_user_detail'),
    
    # Token authentication endpoint
    # Users can POST their email and password to this endpoint to obtain a token.
    path('api-token-auth/', CustomObtainAuthToken.as_view(), name='api_token_auth'),

    # API endpoints for User Registration
    path('api/users/register/', UserRegistrationAPI.as_view(), name='api_user_register'),
]
