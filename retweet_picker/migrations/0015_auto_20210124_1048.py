# Generated by Django 2.2.10 on 2021-01-24 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retweet_picker', '0014_drawprice_queue_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='credit_amount',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='pricingplan',
            name='credit_amount',
            field=models.IntegerField(default=1),
        ),
    ]