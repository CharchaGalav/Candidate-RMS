# Generated by Django 3.2.6 on 2023-12-05 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0073_alter_managerdecision_applicant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='managerdecision',
            name='applicant',
            field=models.CharField(max_length=255),
        ),
    ]
