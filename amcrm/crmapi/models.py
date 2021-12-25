from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.

def get_image_path(instance, filename):
    return os.path.join('customers', str(instance.id), filename)

class Customer(models.Model):
    name = models.CharField(max_length=60, blank=False)
    surname = models.CharField(max_length=60, blank=False)
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

