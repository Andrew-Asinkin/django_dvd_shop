# Generated by Django 3.2.12 on 2025-05-05 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20250330_1454'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-date_order'], 'permissions': (('can_set_status', 'возможность настройки статуса'),), 'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('NEW', 'Новый заказ'), ('APR', 'Подтвержден'), ('PAY', 'Оплачен'), ('CNL', 'Отменен')], default='NEW', max_length=3, verbose_name='Статус'),
        ),
    ]
