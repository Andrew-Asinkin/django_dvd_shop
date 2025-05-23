# Generated by Django 3.2.12 on 2025-03-26 01:38

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True, verbose_name='Код купона')),
                ('value', models.IntegerField(blank=True, help_text='В процентах', null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Размер скидки')),
            ],
            options={
                'verbose_name': 'Скидка',
                'verbose_name_plural': 'Скидки',
                'ordering': ['-value'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('need_delivery', models.BooleanField(verbose_name='Необходимость доставки')),
                ('name', models.CharField(max_length=70, verbose_name='Имя клиента')),
                ('phone', models.CharField(max_length=70, verbose_name='Телефон клиента')),
                ('email', models.EmailField(max_length=254)),
                ('address', models.TextField(blank=True, verbose_name='Адрес')),
                ('notice', models.TextField(blank=True, max_length=150, verbose_name='Примечание')),
                ('date_order', models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')),
                ('date_send', models.DateTimeField(blank=True, null=True, verbose_name='Дата отправки')),
                ('status', models.CharField(choices=[('NEW', 'Новый заказ'), ('APR', 'ПОдтвержден'), ('PAY', 'Оплачен'), ('CNL', 'Отменен')], default='NEW', max_length=3, verbose_name='Статус')),
                ('discount', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.discount', verbose_name='Скидка')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ['-date_order'],
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='В поле необходимо ввести название раздела', max_length=70, unique=True, verbose_name='Название раздела')),
            ],
            options={
                'verbose_name': 'Раздел',
                'verbose_name_plural': 'Разделы',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='В поле необходимо ввести название раздела', max_length=70, unique=True, verbose_name='Название')),
                ('image', models.ImageField(upload_to='images', verbose_name='Изображение')),
                ('price', models.DecimalField(decimal_places='2', max_digits='10', verbose_name='Цена')),
                ('year', models.ImageField(upload_to='', validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2025)])),
                ('country', models.CharField(max_length=70, verbose_name='Страна')),
                ('director', models.CharField(max_length=70, verbose_name='Режиссер')),
                ('play', models.IntegerField(blank=True, help_text='В секундах', null=True, validators=[django.core.validators.MinValueValidator(60)], verbose_name='Продолжительность')),
                ('cast', models.TextField(verbose_name='В ролях')),
                ('description', models.TextField(verbose_name='Описание')),
                ('date', models.DateField(auto_now_add=True, verbose_name='Дата')),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.section', verbose_name='Раздел')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'ordering': ['title', 'year'],
            },
        ),
        migrations.CreateModel(
            name='OrderLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Цена')),
                ('count', models.ImageField(default=1, upload_to='', validators=[django.core.validators.MinValueValidator(1)], verbose_name='Количество')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.order', verbose_name='Заказ')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Стока заказа',
                'verbose_name_plural': 'Строки заказа',
            },
        ),
    ]
