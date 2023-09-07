# Generated by Django 3.2 on 2023-09-08 01:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productreview',
            options={'ordering': ['-created'], 'verbose_name_plural': 'Product Reviews'},
        ),
        migrations.AlterModelOptions(
            name='productsubcategory',
            options={'ordering': ['name'], 'verbose_name_plural': 'Product Sub-categories'},
        ),
        migrations.CreateModel(
            name='CheckoutReceipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkout_summary', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]