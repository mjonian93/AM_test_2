from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
            required=True,
            max_length=32,
    )
    surname = serializers.CharField(
            required=True,
            max_length=32,
    )
    creator = serializers.PrimaryKeyRelatedField(
            read_only=True,
    )

    last_modifier = serializers.IntegerField(
            read_only=True,
    )

    image = serializers.ImageField(
            required=False,
            default=None,
    )

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        validated_data['last_modifier'] = self.context['request'].user.id
        customer = Customer.objects.create(name=validated_data['name'], surname=validated_data['surname'],
                                           creator=validated_data['creator'],
                                           last_modifier=validated_data['last_modifier'], image=validated_data['image'])
        return customer

    class Meta:
        model = Customer
        fields = ('id', 'name', 'surname', 'creator', 'last_modifier', 'image')


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    username = serializers.CharField(
            required=True,
            max_length=32,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(min_length=8, write_only=True)
    is_staff = serializers.BooleanField(default=False)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'],
                                        validated_data['password'], is_staff=validated_data['is_staff'])
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'is_staff')
