# Generated by Django 2.2.10 on 2020-06-03 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_userfeedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='userroles',
            name='role_description',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
