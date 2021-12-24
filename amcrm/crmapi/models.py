from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.

# class User(models.Model):
#     username = models.CharField(max_length=32, blank=False)
#     password = models.CharField(max_length=32, blank=False)
#     id = models.AutoField(primary_key=True)
#     isAdmin = models.BooleanField(default=False, blank=False)

def get_image_path(instance, filename):
    return os.path.join('customers', str(instance.id), filename)

class Customer(models.Model):
    name = models.CharField(max_length=60, blank=False)
    surname = models.CharField(max_length=60, blank=False)
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

# class UserForm(ModelForm):
#     class Meta:
#         model = User
#         widgets = {
#             'password': PasswordInput(),
#         }
#         fields = ['username', 'password', 'isAdmin']
