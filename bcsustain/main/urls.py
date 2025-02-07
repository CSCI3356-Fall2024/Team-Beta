from django.urls import path, include
from .views import (
    signup, login, rewards, supervisorrewards, add_reward, action, base,
    supervisor, landing, campaign_form, profile_setup, manage_supervisors,
    delete_campaign, redeem_reward, logout_view, delete_rewards, complete_campaign, add_permanent_campaign
)
from django.contrib.auth.views import LogoutView
from django.contrib import admin

urlpatterns = [
    path('', login, name='land'),  # Landing page
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('rewards/', rewards, name='rewards'),
    path('rewards/redeem/<int:reward_id>/', redeem_reward, name='redeem_reward'),

    path('supervisorrewards/', supervisorrewards, name='supervisorrewards'),
    path('rewards/delete/', delete_rewards, name='delete_rewards'),

    path('add_reward/', add_reward, name='add_reward'),
    path('action/', action, name='action'),
    path('supervisor/', supervisor, name='supervisor'),
    path('base/', base, name='base'),
    path('landing/', landing, name='landing'),
    path('campaign_form/', campaign_form, name='campaign_form'),

    path('profile_setup/', profile_setup, name='profile_setup'),
    path('campaigns/add_permanent/', add_permanent_campaign, name='add_permanent_campaign'),
    
    path('manage-supervisors/', manage_supervisors, name='manage_supervisors'),
    path('campaign/delete/<int:campaign_id>/', delete_campaign, name='delete_campaign'),
    path('campaign/complete/<int:id>/', complete_campaign, name='complete_campaign'),  # Added path
    path('auth/', include('allauth.urls')),
    path('admin/', admin.site.urls), # Django Admin
    path('accounts/', include('allauth.urls')), # Allauth URLs
    path('rewards/add/', add_reward, name='add_reward'),
]
