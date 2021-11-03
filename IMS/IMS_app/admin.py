from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from IMS_app.models import CustomUser


class UserModel(UserAdmin):
    pass

#This is to register CustomUser Model 
admin.site.register(CustomUser,UserModel)
