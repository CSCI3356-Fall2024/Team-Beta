from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings  # Import settings to use AUTH_USER_MODEL
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps
# Create your models here.


# class CustomUser(AbstractUser):
#     is_supervisor = models.BooleanField(default=False)

#     groups = models.ManyToManyField(
#         'auth.Group',
#         related_name='customuser_set',
#         blank=True,
#         help_text="The groups this user belongs to.",
#         verbose_name="groups",
#     )

class Campaign(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=255)
    description = models.TextField()
    points = models.PositiveIntegerField(default=0)
    delivery_method = models.CharField(
        max_length=50,
        choices=[
            ('QR Code', 'QR Code'),
            ('Photo Validation', 'Photo Validation'),
            ('Integration', 'Integration'),
        ],
        default='QR Code'
    )
    add_to_news = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# class Profile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     is_supervisor = models.BooleanField(default=False) #added by Jonathan
#     school = models.CharField(max_length=255)
#     graduation_year = models.IntegerField()
#     major1 = models.CharField(max_length=255)
#     major2 = models.CharField(max_length=255, blank=True, null=True)
#     profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

#     def __str__(self):
#         return f"{self.user.username}'s Profile"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_supervisor = models.BooleanField(default=False)
    school = models.CharField(max_length=255)
    graduation_year = models.IntegerField(blank=True, null=True)
    major1 = models.CharField(max_length=255)
    major2 = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

# Signal to create a Profile for each new User
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


#delete probably
def get_profile(user):
    Profile = apps.get_model('main', 'Profile')  # Dynamically get the Profile model
    profile, created = Profile.objects.get_or_create(user=user)
    return profile

# Attach this property to User
User.add_to_class('profile', property(get_profile))