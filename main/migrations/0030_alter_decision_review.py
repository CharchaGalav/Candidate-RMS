# Generated by Django 3.2.6 on 2023-11-22 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0029_alter_decision_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='decision',
            name='review',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='decision_review', to='main.meetingreview'),
        ),
    ]
