from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from band.models import Musician,Band,Venue, Room,UserProfile
from datetime import date,datetime


        
class UserProfileinline(admin.StackedInline):
    model = UserProfile 
    can_delete = False
class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileinline]