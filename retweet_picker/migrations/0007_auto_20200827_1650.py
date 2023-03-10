# Generated by Django 2.2.10 on 2020-08-27 20:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('retweet_picker', '0006_giveawayqueue'),
    ]

    operations = [
        migrations.AddField(
            model_name='giveawayqueue',
            name='giveaway_amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='giveawayqueue',
            name='queue_type',
            field=models.CharField(choices=[('D', 'Default'), ('L', 'Low'), ('H', 'High')], max_length=1),
        ),
        migrations.AlterField(
            model_name='giveawaystats',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.OrderItem'),
        ),
    ]
