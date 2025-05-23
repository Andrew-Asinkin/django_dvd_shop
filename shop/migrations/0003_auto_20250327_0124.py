# Generated by Django 3.2.12 on 2025-03-27 01:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20250327_0120'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(null=True, upload_to='images', verbose_name='Изображение'),
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places='2', max_digits='10', null=True, verbose_name='Цена'),
        ),
        migrations.AddField(
            model_name='product',
            name='year',
            field=models.ImageField(null=True, upload_to='', validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2025)]),
        ),
    ]
