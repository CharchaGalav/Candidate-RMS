# Generated by Django 3.2.6 on 2023-11-22 06:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_alter_meetingreview_decision'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meetingreview',
            name='reviewer',
        ),
    ]
