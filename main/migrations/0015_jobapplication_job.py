# Generated by Django 3.2.6 on 2023-11-19 15:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20231119_0149'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobapplication',
            name='job',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.job'),
        ),
    ]
