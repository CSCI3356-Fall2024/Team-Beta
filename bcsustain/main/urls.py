from django.urls import path, include
from .views import signup, login, rewards, supervisorrewards, add_reward, action, base, supervisor, landing, campaign_form, profile_setup, manage_supervisors, delete_campaign
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('',login, name='land'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
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
    path('campaign/delete/<int:campaign_id>/', delete_campaign, name='delete_campaign'),
    path('auth/', include('social_django.urls', namespace='social')),
]
