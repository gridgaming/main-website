# Generated by Django 2.2.10 on 2020-07-24 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('giveaways', '0004_auto_20200722_1212'),
    ]

    operations = [
        migrations.AddField(
            model_name='giveawaypkandslug',
            name='description',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
