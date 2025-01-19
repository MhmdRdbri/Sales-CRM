# Generated by Django 5.0.6 on 2024-11-20 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customerprofile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField()),
                ('text', models.TextField()),
                ('send_time', models.DateTimeField()),
                ('send_date', models.DateTimeField()),
                ('audiences', models.ManyToManyField(blank=True, related_name='notice', to='customerprofile.customerprofile')),
            ],
        ),
    ]
