from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings  # Import settings to use AUTH_USER_MODEL

# Create your models here.

class CustomUser(AbstractUser):
    is_supervisor = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )

class Campaign(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=255)
    description = models.TextField()
    points = models.PositiveIntegerField(default=0)  # Integer field with a default value
    delivery_method = models.CharField(
        max_length=50,
        choices=[
            ('QR Code', 'QR Code'),
            ('Photo Validation', 'Photo Validation'),
            ('Integration', 'Integration'),
        ],
        default='QR Code'  # String field with default value 'QR Code'
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_supervisor = models.BooleanField(default=False) #added by Jonathan
    school = models.CharField(max_length=255)
    graduation_year = models.IntegerField()
    major1 = models.CharField(max_length=255)
    major2 = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
