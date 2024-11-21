# Generated by Django 5.1.2 on 2024-11-21 05:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Campaign",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("location", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("points", models.PositiveIntegerField(default=0)),
                (
                    "delivery_method",
                    models.CharField(
                        choices=[
                            ("QR Code", "QR Code"),
                            ("Photo Validation", "Photo Validation"),
                            ("Integration", "Integration"),
                        ],
                        default="QR Code",
                        max_length=50,
                    ),
                ),
                ("add_to_news", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="campaign_images/"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Reward",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("points_required", models.PositiveIntegerField()),
                ("available", models.BooleanField(default=True)),
                ("expiration_date", models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "google_username",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "google_email",
                    models.EmailField(
                        blank=True, max_length=254, null=True, unique=True
                    ),
                ),
                ("graduation_year", models.PositiveIntegerField(blank=True, null=True)),
                ("points", models.PositiveIntegerField(default=0)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
