# Generated by Django 5.1.2 on 2024-11-04 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_profile_graduation_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='graduation_year',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]