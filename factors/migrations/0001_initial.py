# Generated by Django 5.0.6 on 2024-11-03 15:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customerprofile', '0001_initial'),
        ('products', '0002_category_alter_product_product_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Factors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conttract_date', models.DateTimeField(auto_now_add=True)),
                ('price', models.IntegerField()),
                ('description', models.TextField()),
                ('costumer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='factor', to='customerprofile.customerprofile')),
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
