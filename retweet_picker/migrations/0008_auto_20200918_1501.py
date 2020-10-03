# Generated by Django 2.2.10 on 2020-09-18 19:01

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('retweet_picker', '0007_auto_20200827_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='giveawaywinners',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='giveawaywinners',
            name='giveaway_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='draw_giveaway_details', to='retweet_picker.TwitterGiveawayID'),
        ),
        migrations.AddField(
            model_name='giveawaywinners',
            name='participants',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='giveawaywinners',
            name='re_rolls',
            field=models.ManyToManyField(related_name='draw_rerolled_user', to='retweet_picker.ContestUserAccounts'),
        ),
        migrations.AlterField(
            model_name='giveawaywinners',
            name='winner',
            field=models.ManyToManyField(related_name='draw_giveaway_winner', to='retweet_picker.ContestUserAccounts'),
        ),
    ]
