from django.shortcuts import redirect
from django.urls import reverse

def ensure_profile_completion(backend, user, *args, **kwargs):
    # Redirect to profile setup page if the user's profile is incomplete
    if user.is_authenticated and not hasattr(user, 'profile') or not user.profile.is_complete:
        return redirect(reverse('profile_setup'))
