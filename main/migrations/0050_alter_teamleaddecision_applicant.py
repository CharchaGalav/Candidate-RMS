# Generated by Django 3.2.6 on 2023-11-23 15:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0049_teamleaddecision_log'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teamleaddecision',
            name='applicant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='decision_review', to='main.jobapplication'),
        ),
    ]
