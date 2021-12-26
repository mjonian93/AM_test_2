from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from rest_framework.parsers import MultiPartParser

from .serializers import CustomerSerializer, UserSerializer
from .models import Customer

# Create your views here.

class CustomerAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, )

    def post(self, request):
        serializer = CustomerSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None):
        if id:
            customer = Customer.objects.get(id=id)
            serializer = CustomerSerializer(customer)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def patch(self, request, id=None):
        if id:
            instance = Customer.objects.get(id=id)
            instance.last_modifier = request.user.id
            instance.save()
        customer = Customer.objects.get(id=id)
        serializer = CustomerSerializer(customer, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors})

    def delete(self, request, id=None):
        customer = get_object_or_404(Customer, id=id)
        customer.delete()
        return Response({"status": "success", "data": "Item Deleted"})

class UserAPIView(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None):
        if id:
            user = User.objects.get(id=id)
            serializer = UserSerializer(user)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def patch(self, request, id=None):
        user = User.objects.get(id=id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors})

    def delete(self, request, id=None):
        user = get_object_or_404(User, id=id)
        user.delete()
        return Response({"status": "success", "data": "Item Deleted"})





