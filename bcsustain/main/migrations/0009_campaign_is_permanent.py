# Generated by Django 5.1.2 on 2024-12-15 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_profile_points_spent'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='is_permanent',
            field=models.BooleanField(default=False),
        ),
    ]
