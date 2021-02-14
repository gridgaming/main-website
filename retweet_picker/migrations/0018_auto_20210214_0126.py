# Generated by Django 2.2.10 on 2021-02-14 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retweet_picker', '0017_auto_20210203_0905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='giveawaywinners',
            name='drawed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='giveawaywinners',
            name='participants',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='giveawaywinners',
            name='re_rolls',
            field=models.ManyToManyField(blank=True, to='retweet_picker.Rerolls'),
        ),
        migrations.AlterField(
            model_name='giveawaywinners',
            name='winner',
            field=models.ManyToManyField(blank=True, related_name='draw_giveaway_winner', to='retweet_picker.ContestUserAccounts'),
        ),
    ]
