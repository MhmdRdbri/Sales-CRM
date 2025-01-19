# Generated by Django 5.0.6 on 2025-01-15 11:04

import multiselectfield.db.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0006_marketing_target_rank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marketing',
            name='target_rank',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('RE', 'Red'), ('GR', 'Gray'), ('GO', 'Gold'), ('SS', 'Super Special')], help_text='Select the target ranks for this campaign.', max_length=11),
        ),
    ]
