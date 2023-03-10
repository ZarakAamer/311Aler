# Generated by Django 4.1.4 on 2023-01-19 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_price_is_popular_property_email_property_email1_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='property',
            old_name='address',
            new_name='house_number',
        ),
        migrations.RenameField(
            model_name='property',
            old_name='job_name',
            new_name='street_name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='is_yearly',
        ),
        migrations.AddField(
            model_name='property',
            name='zip_code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
