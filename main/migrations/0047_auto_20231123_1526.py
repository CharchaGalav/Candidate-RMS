# Generated by Django 3.2.6 on 2023-11-23 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0046_alter_meetingschedule_job_application'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jobapplication',
            old_name='timestamp',
            new_name='logs',
        ),
        migrations.AddField(
            model_name='meetingschedule',
            name='logs',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
