# Generated by Django 5.0.6 on 2024-11-26 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notice', '0003_alter_notice_send_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='notice',
            name='task_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
