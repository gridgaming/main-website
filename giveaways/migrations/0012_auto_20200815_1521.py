# Generated by Django 2.2.10 on 2020-08-15 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('giveaways', '0011_auto_20200807_1219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='giveaway',
            name='visible',
            field=models.BooleanField(default=True),
        ),
    ]
