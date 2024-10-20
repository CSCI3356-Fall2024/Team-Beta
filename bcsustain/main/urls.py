from django.urls import path
from .views import signup, login, rewards, supervisorrewards, add_reward

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('rewards/', rewards, name='rewards'),
    path('supervisorrewards/', supervisorrewards, name='supervisorrewards'),
    path('add_reward/', add_reward, name='add_reward')
]
