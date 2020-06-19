# Generated by Django 2.2.10 on 2020-06-02 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_item_priority'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='sponsor_supplier',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='account_type',
            field=models.CharField(blank=True, choices=[('S', 'Sponsor Provider'), ('C', 'Content Creator'), ('R', 'Regular User')], default='R', max_length=1, null=True),
        ),
    ]
