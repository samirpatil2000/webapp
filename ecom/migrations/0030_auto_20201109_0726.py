# Generated by Django 3.1.1 on 2020-11-09 07:26

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0029_auto_20201108_1426'),
    ]

    operations = [
        migrations.CreateModel(
            name='IP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('ip_address', models.GenericIPAddressField()),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='ordered_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 9, 7, 26, 8, 300124, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='trans_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 9, 7, 26, 8, 301242, tzinfo=utc)),
        ),
    ]
