# Generated by Django 2.2.10 on 2020-10-13 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retweet_picker', '0009_auto_20201008_1438'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='giveawaywinners',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='rerolls',
            options={'ordering': ['id']},
        ),
        migrations.AddField(
            model_name='giveawaywinners',
            name='winner_count',
            field=models.IntegerField(default=1),
        ),
    ]
