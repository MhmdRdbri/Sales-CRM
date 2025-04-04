# Generated by Django 5.0.6 on 2025-01-11 11:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customerprofile', '0006_customerprofile_address_customerprofile_description_and_more'),
        ('factors', '0004_alter_factors_description_alter_factors_files'),
    ]

    operations = [
        migrations.CreateModel(
            name='Factor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_date', models.DateTimeField(auto_now_add=True)),
                ('price', models.IntegerField()),
                ('description', models.TextField(blank=True, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='factor_files/')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='factors', to='customerprofile.customerprofile')),
            ],
        ),
        migrations.AlterField(
            model_name='factoritem',
            name='factor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='factors.factor'),
        ),
        migrations.DeleteModel(
            name='Factors',
        ),
    ]
