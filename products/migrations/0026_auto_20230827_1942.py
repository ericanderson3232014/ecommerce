# Generated by Django 3.2 on 2023-08-27 19:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0025_auto_20230827_1858'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('phone_number', models.IntegerField()),
                ('address', models.CharField(max_length=1000)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('province', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(max_length=100)),
                ('zip_code', models.IntegerField()),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Addresses',
            },
        ),
        migrations.DeleteModel(
            name='Address',
        ),
    ]