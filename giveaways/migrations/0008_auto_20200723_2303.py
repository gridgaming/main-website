# Generated by Django 2.2.10 on 2020-07-24 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('giveaways', '0007_giveawaypkandslug_giveaway_end_date'),
    ]

    operations = [
        migrations.DeleteModel(
            name='GiveawayPkAndSlug',
        ),
        migrations.AddField(
            model_name='giveaway',
            name='description',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='giveaway',
            name='giveaway_end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='giveaway',
            name='slug',
            field=models.SlugField(default='', editable=False, max_length=350),
        ),
        migrations.AlterField(
            model_name='giveaway',
            name='title',
            field=models.CharField(max_length=350),
        ),
    ]
