# Generated by Django 2.2.10 on 2021-02-01 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retweet_picker', '0015_auto_20210124_1048'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='analyzed_time',
            field=models.DateTimeField(null=True),
        ),
    ]
