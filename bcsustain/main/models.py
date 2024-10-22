from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.

class CustomUser(AbstractUser):
    is_supervisor = models.BooleanField(default=False)

    # Add related_name to avoid clashes with auth.User
    # groups = models.ManyToManyField(
    #     'auth.Group',
    #     related_name='customuser_set',  # This avoids the clash
    #     blank=True,
    #     help_text='The groups this user belongs to.',
    #     verbose_name='groups'
    # )
    
    # user_permissions = models.ManyToManyField(
    #     'auth.Permission',
    #     related_name='customuser_set_permissions',  # This avoids the clash
    #     blank=True,
    #     help_text='Specific permissions for this user.',
    #     verbose_name='user permissions'
    # )

class Campaign(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=True)  # Field to mark campaigns as active/inactive

    def __str__(self):
        return self.name
