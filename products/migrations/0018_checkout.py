# Generated by Django 3.2 on 2023-08-25 06:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0017_rename_total_order_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkout_datte', models.DateTimeField(auto_now_add=True)),
                ('total_amount_due', models.DecimalField(decimal_places=0, max_digits=10)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('order', models.ManyToManyField(to='products.Order')),
            ],
        ),
    ]
