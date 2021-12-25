from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
import os

# Create your models here.

def get_image_path(instance, filename):
    return os.path.join('customers', str(instance.id), filename)

class Customer(models.Model):
    name = models.CharField(max_length=60, blank=False)
    surname = models.CharField(max_length=60, blank=False)
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Model Save override
    def save(self, *args, **kwargs):
        if self.id is None:
            saved_image = self.image
            self.image = None
            super(Customer, self).save(*args, **kwargs)
            self.image = saved_image
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')

        super(Customer, self).save(*args, **kwargs)

@receiver(pre_delete, sender=Customer)
def customer_delete(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(False)


