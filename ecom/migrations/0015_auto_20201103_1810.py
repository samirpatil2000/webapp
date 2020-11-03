# Generated by Django 3.1.1 on 2020-11-03 18:10

import datetime
import django.core.validators
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0014_auto_20201103_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='mobile_number',
            field=models.IntegerField(default='1234567890', validators=[django.core.validators.MinValueValidator(9), django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.AlterField(
            model_name='address',
            name='zipcode',
            field=models.IntegerField(default='400035', validators=[django.core.validators.MinValueValidator(5), django.core.validators.MaxValueValidator(6)]),
        ),
        migrations.AlterField(
            model_name='order',
            name='ordered_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 3, 18, 10, 52, 780487, tzinfo=utc)),
        ),
    ]
