# Generated by Django 2.2.10 on 2020-05-30 05:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('retweet_picker', '0004_giveawaystats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='giveawayresults',
            name='giveaway_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='giveaway_details', to='retweet_picker.TwitterGiveawayID'),
        ),
        migrations.AlterField(
            model_name='giveawaystats',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Order'),
        ),
    ]
