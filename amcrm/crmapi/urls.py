from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import CustomerAPIView, UserAPIView

urlpatterns = [
    path('customers/', CustomerAPIView.as_view(), name='api_customer'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('users/', UserAPIView.as_view(), name='api_user')
]