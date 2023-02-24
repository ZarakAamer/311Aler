# Generated by Django 4.1.4 on 2023-01-11 20:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='pro_expiry_date',
            new_name='pro_start_date',
        ),
        migrations.AddField(
            model_name='price',
            name='descripion',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='price',
            name='is_yearly',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='price',
            name='token',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='is_yearly',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='strip_costumer_token',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='price',
            name='number_of_properties',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='price',
            name='price_per_month',
            field=models.IntegerField(null=True),
        ),
        migrations.CreateModel(
            name='UserCredsSaver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=115)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
