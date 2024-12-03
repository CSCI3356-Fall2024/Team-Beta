from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
#from .models import CustomUser
from .models import Campaign, Profile, Reward, Event

"""
# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
       (None, {'fields': ('is_supervisor',)}),
    )
"""

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'location', 'is_active')  # Customize what is shown in the admin list

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'google_email', 'graduation_year', 'points', 'is_supervisor')

@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ('name', 'points_required', 'available')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'points')
