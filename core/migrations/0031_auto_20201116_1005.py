# Generated by Django 2.2.10 on 2020-11-16 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_auto_20201107_0002'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_id',
            field=models.IntegerField(default=0),
        ),
    ]
