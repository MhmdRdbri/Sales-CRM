# Generated by Django 5.0.6 on 2024-11-12 07:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customerprofile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Marketing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campaign_name', models.CharField()),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('message', models.TextField()),
                ('target_audiences', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='marketing', to='customerprofile.customerprofile')),
            ],
        ),
    ]
