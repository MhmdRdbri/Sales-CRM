# customerprofile/migrations/0001_initial.py
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='CustomerProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=255, unique=True)),
                ('date_of_birth', models.DateField(null=True, blank=True)),
                ('email', models.CharField(max_length=255, null=True, blank=True)),
                ('telegram_id', models.CharField(max_length=255, null=True, blank=True)),
                ('national_id', models.BigIntegerField(null=True, blank=True)),
                ('address', models.TextField(null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('created_at', models.DateTimeField(default='django.utils.timezone.now')),
                ('instagram_id', models.CharField(max_length=255, null=True, blank=True)),
                ('buyer_rank', models.CharField(
                    max_length=2, 
                    choices=[('RE', 'Red'), ('GR', 'Gray'), ('GO', 'Gold'), ('SS', 'Super Special')],
                    default='RE',
                    blank=True
                )),
                ('customer_picture', models.ImageField(upload_to='customer_profile_pictures/', null=True, blank=True)),
            ],
        ),
    ]
