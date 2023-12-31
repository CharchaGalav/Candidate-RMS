# Generated by Django 3.2.6 on 2023-11-22 13:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0032_rename_applicant_name_decision_applicant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='decision',
            name='applicant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='decision_review', to=settings.AUTH_USER_MODEL),
        ),
    ]
