from django.contrib import admin
from .models import User, UserForm, Customer

class UserAdmin(admin.ModelAdmin):
    form = UserForm

admin.site.register(User, UserAdmin)
admin.site.register(Customer)

# Register your models here.
