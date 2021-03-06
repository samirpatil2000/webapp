# Generated by Django 3.1.1 on 2020-12-14 13:17

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0031_auto_20201214_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='cat_images'),
        ),
        migrations.AlterField(
            model_name='ip',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 14, 13, 17, 10, 981350, tzinfo=utc), verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='order',
            name='ordered_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 14, 13, 17, 10, 983016, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='trans_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 14, 13, 17, 10, 984157, tzinfo=utc)),
        ),
    ]
