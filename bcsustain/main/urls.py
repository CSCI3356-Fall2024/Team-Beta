from django.urls import path
from .views import signup, login, rewards, supervisorrewards, add_reward, action, base, supervisor, landing, campaign_form, profile_setup, manage_supervisors, confirm_delete

urlpatterns = [
    path('',login, name='land'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('rewards/', rewards, name='rewards'),
    path('supervisorrewards/', supervisorrewards, name='supervisorrewards'),
    path('add_reward/', add_reward, name='add_reward'),
    path('action/', action, name = 'action'),
    path('supervisor/', supervisor, name = 'supervisor'),
    path('base/', base, name = 'base'),
    path('landing/', landing, name = 'landing'),
    path('campaign_form/', campaign_form, name = 'campaign_form'),
    path('profile_setup/', profile_setup, name = 'profile_setup'),
    path('manage-supervisors/', manage_supervisors, name='manage_supervisors'),
    path('confirm_delete/', confirm_delete, name='confirm_delete'),

]
