from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import CustomerAPIView, UserAPIView

urlpatterns = [
    path('customers/', CustomerAPIView.as_view(), name='api_customer'),
    path('customers/<int:id>', CustomerAPIView.as_view(), name='api_customer_indexed'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('users/', UserAPIView.as_view(), name='api_user'),
    path('users/<int:id>', UserAPIView.as_view(), name='api_user_indexed')
]