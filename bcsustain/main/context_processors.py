from django.contrib.auth.models import AnonymousUser

def add_is_supervisor(request):
    """
    Add a context variable 'is_supervisor' to indicate if the user is a supervisor.
    """
    if not request.user or isinstance(request.user, AnonymousUser):
        return {'is_supervisor': False}

    # Assuming `is_supervisor` is a field in the user's profile
    return {'is_supervisor': getattr(request.user.profile, 'is_supervisor', False)}
