# Generated by Django 3.1.1 on 2020-11-07 09:33

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0022_auto_20201106_1351'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='payment_method',
            field=models.CharField(default='COD', max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='ordered_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 7, 9, 33, 34, 774009, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='trans_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 7, 9, 33, 34, 775196, tzinfo=utc)),
        ),
    ]
