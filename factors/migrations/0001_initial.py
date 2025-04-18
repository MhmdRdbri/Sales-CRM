# Generated by Django 5.0.6 on 2025-01-15 11:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customerprofile', '0001_initial'),
        ('products', '0004_alter_product_color_alter_product_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Factors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_date', models.DateTimeField(auto_now_add=True)),
                ('price', models.IntegerField()),
                ('description', models.TextField(blank=True, null=True)),
                ('files', models.FileField(blank=True, null=True, upload_to='factors_files/')),
                ('costumer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='factor', to='customerprofile.customerprofile')),
            ],
        ),
        migrations.CreateModel(
            name='FactorItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('factor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='factors.factors')),
            ],
        ),
    ]
