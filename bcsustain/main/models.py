from django.db import models

# Create your models here.
class Campaign(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=True)  # Field to mark campaigns as active/inactive

    def __str__(self):
        return self.name
