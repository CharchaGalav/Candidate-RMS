# Generated by Django 3.2.6 on 2023-12-28 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0094_alter_meetingschedule_scheduled_meet_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='is_onboardingHr',
        ),
    ]
