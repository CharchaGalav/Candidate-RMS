# Generated by Django 3.2.6 on 2023-11-18 20:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_remove_jobapplication_job'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobapplication',
            name='user',
        ),
        migrations.AddField(
            model_name='jobapplication',
            name='job',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.job'),
        ),
    ]