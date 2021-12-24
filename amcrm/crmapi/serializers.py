from rest_framework import serializers

from .models import Customer

#class UserSerializer(serializers.HyperlinkedModelSerializer):
#    class Meta:
#        model = User
#        fields = ('id', 'username', 'password', 'isAdmin')

class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'name', 'surname', 'image', 'creator')