# Generated by Django 2.2.10 on 2020-10-07 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_userroles_role_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='blacklisted',
            field=models.BooleanField(default=False, null=True),
        ),
    ]