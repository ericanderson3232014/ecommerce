# Generated by Django 3.2 on 2023-08-16 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_productreview_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='productreview',
            name='rating',
            field=models.CharField(choices=[('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5)], default=1, max_length=10),
            preserve_default=False,
        ),
    ]
