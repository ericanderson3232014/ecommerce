# Generated by Django 3.2 on 2023-09-05 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0028_auto_20230905_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkout',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
