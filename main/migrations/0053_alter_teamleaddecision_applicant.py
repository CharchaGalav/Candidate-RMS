# Generated by Django 3.2.6 on 2023-11-23 15:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0052_alter_teamleaddecision_applicant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teamleaddecision',
            name='applicant',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='decision_review', to=settings.AUTH_USER_MODEL),
        ),
    ]
