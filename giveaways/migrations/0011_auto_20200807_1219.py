# Generated by Django 2.2.10 on 2020-08-07 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('giveaways', '0010_giveaway_gleam_graph_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='giveaway',
            name='sponsored',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='giveaway',
            name='visible',
            field=models.BooleanField(default=False),
        ),
    ]
