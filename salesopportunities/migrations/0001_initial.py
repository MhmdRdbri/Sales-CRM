# Generated by Django 5.0.6 on 2024-11-02 11:01

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
            name='SalesOpportunity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follow_up_date', models.DateField()),
                ('estimated_amount', models.BigIntegerField()),
                ('opportunity_priority', models.CharField(choices=[('low_priority', 'low_priority'), ('mid_priority', 'mid_priority'), ('high_priority', 'high_priority')], max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales_opportunities', to='customerprofile.customerprofile')),
                ('selected_products', models.ManyToManyField(related_name='sales_opportunities', to='products.product')),
            ],
        ),
    ]
