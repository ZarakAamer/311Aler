# Generated by Django 4.1.4 on 2023-01-28 11:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_voilation_v_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='email',
        ),
        migrations.RemoveField(
            model_name='property',
            name='email1',
        ),
        migrations.RemoveField(
            model_name='property',
            name='email2',
        ),
        migrations.RemoveField(
            model_name='property',
            name='fname',
        ),
        migrations.RemoveField(
            model_name='property',
            name='fname1',
        ),
        migrations.RemoveField(
            model_name='property',
            name='fname2',
        ),
        migrations.RemoveField(
            model_name='property',
            name='house_number',
        ),
        migrations.RemoveField(
            model_name='property',
            name='lname',
        ),
        migrations.RemoveField(
            model_name='property',
            name='lname1',
        ),
        migrations.RemoveField(
            model_name='property',
            name='lname2',
        ),
        migrations.RemoveField(
            model_name='property',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='property',
            name='phone1',
        ),
        migrations.RemoveField(
            model_name='property',
            name='phone2',
        ),
        migrations.RemoveField(
            model_name='property',
            name='state',
        ),
        migrations.RemoveField(
            model_name='property',
            name='street_name',
        ),
        migrations.RemoveField(
            model_name='property',
            name='zip_code',
        ),
        migrations.CreateModel(
            name='AdditionalContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=255, null=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to='main.property')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
