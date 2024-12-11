from allauth.account.signals import user_logged_in
from django.dispatch import receiver
from .models import Profile
from allauth.socialaccount.models import SocialAccount
import logging

logger = logging.getLogger(__name__)

@receiver(user_logged_in)
def update_profile_on_login(sender, request, user, **kwargs):
    try:
        social_account = SocialAccount.objects.get(user=user, provider='google')
        profile, created = Profile.objects.get_or_create(user=user)
        profile.google_username = social_account.extra_data.get('name')
        logger.warning("Hello world")
        profile.google_email = social_account.extra_data.get('email')
        profile.save()
    except SocialAccount.DoesNotExist:
        pass