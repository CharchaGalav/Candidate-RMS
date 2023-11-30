# Generated by Django 3.2.6 on 2023-11-18 20:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20231119_0133'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobapplication',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='jobapplication',
            name='job',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.job'),
        ),
    ]
