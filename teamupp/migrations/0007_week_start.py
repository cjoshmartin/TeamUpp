# Generated by Django 3.2.4 on 2021-06-21 01:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamupp', '0006_auto_20210621_0056'),
    ]

    operations = [
        migrations.AddField(
            model_name='week',
            name='start',
            field=models.DateField(default=datetime.date(2021, 6, 21)),
            preserve_default=False,
        ),
    ]
