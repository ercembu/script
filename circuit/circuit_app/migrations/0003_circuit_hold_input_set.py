# Generated by Django 2.2.dev20181217100344 on 2018-12-22 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('circuit_app', '0002_auto_20181220_0842'),
    ]

    operations = [
        migrations.AddField(
            model_name='circuit_hold',
            name='input_set',
            field=models.BooleanField(default=False),
        ),
    ]
