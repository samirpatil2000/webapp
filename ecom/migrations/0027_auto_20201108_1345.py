# Generated by Django 3.1.1 on 2020-11-08 13:45

import datetime
import django.core.validators
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0026_auto_20201108_1343'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='address_mobile_number',
            new_name='address_mobile_number_verified',
        ),
        migrations.AddField(
            model_name='transaction',
            name='address_mobile_number_2',
            field=models.IntegerField(blank=True, default='1234567890', null=True, validators=[django.core.validators.MinValueValidator(999999999), django.core.validators.MaxValueValidator(9999999999)]),
        ),
        migrations.AlterField(
            model_name='order',
            name='ordered_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 8, 13, 45, 51, 593992, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='trans_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 8, 13, 45, 51, 595127, tzinfo=utc)),
        ),
    ]
