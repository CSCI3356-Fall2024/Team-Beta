from django.contrib.auth.models import AnonymousUser

def add_is_supervisor(request):
    """
    Add a context variable 'is_supervisor' to indicate if the user is a supervisor.
    """
    if not request.user or isinstance(request.user, AnonymousUser):
        return {'is_supervisor': False}

    # Assuming `is_supervisor` is a field in the user's profile
    return {'is_supervisor': getattr(request.user.profile, 'is_supervisor', False)}

from .models import Profile

def add_profile_picture(request):
    if request.user.is_authenticated:
        try:
            profile_picture_url = request.user.profile.profile_picture.url
        except (AttributeError, ValueError):
            profile_picture_url = '/static/default_profile_pic.png'
        print(f"Navbar Profile Picture URL: {profile_picture_url}")  # Debugging
        return {'navbar_profile_picture': profile_picture_url}
    return {'navbar_profile_picture': '/static/default_profile_pic.png'}
