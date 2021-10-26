# Generated by Django 3.2.6 on 2021-10-25 09:35

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_auto_20211025_1617'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='votes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='question',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 26, 9, 35, 36, 705191, tzinfo=utc), verbose_name='date end'),
        ),
        migrations.DeleteModel(
            name='Vote',
        ),
    ]
