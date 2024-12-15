#models.py is the data layer
#Models are python classes that represent data tables
#includes fields that correspond to table columns
#includes methods for manipulating data
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps


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
    is_permanent = models.BooleanField(default=False)  # New field for permanent campaigns
    image = models.ImageField(upload_to='campaign_images/', blank=True, null=True)

    def get_image_url(self):
        if self.image:
            return self.image.url
        return '/static/green2go.png'

    def __str__(self):
        return self.name



class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    google_username = models.CharField(max_length=100, null=True, blank=True)
    google_email = models.EmailField(unique=True, null=True, blank=True)
    school = models.CharField(max_length=100, default="Boston College", null=True, blank=True)
    graduation_year = models.PositiveIntegerField(null=True, blank=True)
    points = models.PositiveIntegerField(default=0)  # Points earned (used for the leaderboard)
    points_spent = models.PositiveIntegerField(default=0)  # Track points spent on rewards
    major1 = models.CharField(max_length=100, null=True, blank=True)
    major2 = models.CharField(max_length=100, default="N/A", null=True)
    is_supervisor = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True, default='profile_pictures/default_profile_pic.png')

    def total_points(self):
        """Calculate the total points after deducting the points spent."""
        return self.points - self.points_spent

    def __str__(self):
        return f"{self.user.username}'s Profile - {self.total_points()} points"

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


class Reward(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    points_required = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    expiration_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def is_available(self):
        from django.utils import timezone
        return self.is_active and (self.expiration_date is None or self.expiration_date >= timezone.now().date())

    def __str__(self):
        return f"{self.name} - {self.points_required} points"


class RedeemedReward(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='redeemed_rewards')
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE, related_name='redemptions')
    redeemed_at = models.DateTimeField(auto_now_add=True)
    points_spent = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} redeemed {self.reward.name} on {self.redeemed_at}"


class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateTimeField()
    points = models.PositiveIntegerField(default=0)
    description = models.TextField()
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)

    def __str__(self):
        return self.name
