# Generated by Django 3.2.6 on 2023-12-13 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0080_jobapplication_mainhr_to_hr'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobapplication',
            name='meetscheduled_by_hr',
            field=models.BooleanField(default=False),
        ),
    ]
