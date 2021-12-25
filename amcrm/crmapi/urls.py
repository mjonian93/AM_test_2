from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import CustomerAPIView

urlpatterns = [
    #path('users/', UserAPIView.as_view()),
    path('customers/', CustomerAPIView.as_view()),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth')
]