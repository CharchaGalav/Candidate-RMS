# Generated by Django 3.2.6 on 2023-12-23 12:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0087_jobapplication_logs'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcceptanceDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_of_acceptance', models.CharField(max_length=255)),
                ('reason', models.TextField()),
                ('accepted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('job_application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.jobapplication')),
            ],
        ),
        migrations.DeleteModel(
            name='TeamLeadDecision',
        ),
    ]
