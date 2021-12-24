from django.urls import path
from .views import CustomerAPIView

urlpatterns = [
    #path('users/', UserAPIView.as_view()),
    path('customers/', CustomerAPIView.as_view())
]