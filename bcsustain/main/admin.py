from django.contrib import admin
from .models import Campaign

<<<<<<< HEAD
# Register your models here.
=======
@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'location', 'is_active')  # Customize what is shown in the admin list
>>>>>>> 00c3447b7542e9af483689653449f6ca6d1fa11a
