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
    image = models.ImageField(upload_to='campaign_images/', blank=True, null=True)

    def get_image_url(self):
        # If no image is uploaded, use the default image
        if self.image:
            return self.image.url
        return '/static/green2go.png'  # Path to the default image in the static folder

    def __str__(self):
        return self.name


#commenting out previous profile code to make the new profile homogenous with Samary's code - Almany

# class Profile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     is_supervisor = models.BooleanField(default=False)
#     school = models.CharField(max_length=255, blank=True, null=True)
#     graduation_year = models.IntegerField(blank=True, null=True)
#     major1 = models.CharField(max_length=255, blank=True, null=True)
#     major2 = models.CharField(max_length=255, blank=True, null=True)
#     profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

#     def __str__(self):
#         return f"{self.user.username}'s Profile"

#     def is_complete(self):
#         return bool(self.school and self.graduation_year and self.major1)


# # Signal to create a Profile for each new User


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

#New profile model based from Samary
#I recognize that further changes may be required later on, especially to relevant HTML and CSS pages - Almany
class Profile(models.Model):
    #User is now an object
    #Casacade allows for anything related to the user to be deleted. We want deleted data to be balanced. - Almany
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'profile')
    #Name and email from google is saved here - Almany
    google_username = models.CharField(max_length=100, null = True, blank = True)
    google_email = models.EmailField(unique= True, null = True, blank = True)
    graduation_year = models.PositiveIntegerField(null=True, blank = True)
    points = models.PositiveIntegerField(default=0)
    is_supervisor = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Profile - {self.points} points"
    
    def is_complete(self):
        return bool(self.google_username and self.google_email and self.graduation_year)

@receiver(post_save,sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
    #else:
        #instance.profile.save() #if the user already exists, the profile is saved

#Will code below be relevant? - Almany
#delete probably
def get_profile(user):
    Profile = apps.get_model('main', 'Profile')  # Dynamically get the Profile model
    profile, created = Profile.objects.get_or_create(user=user)
    return profile

# Attach this property to User
User.add_to_class('profile', property(get_profile))

#Jacob added this
class Reward(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    points_required = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    expiration_date = models.DateField(null=True, blank=True)  # Add this line
    is_active = models.BooleanField(default=True)  # Ensure this field exists
    def is_available(self):
        from django.utils import timezone
        return self.is_active and (self.expiration_date is None or self.expiration_date >= timezone.now().date())


    def __str__(self):
        return self.name
    
class RedeemedReward(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='redeemed_rewards')
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE, related_name='redemptions')
    redeemed_at = models.DateTimeField(auto_now_add=True)
    points_spent = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} redeemed {self.reward.name} on {self.redeemed_at}"