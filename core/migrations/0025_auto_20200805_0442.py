# Generated by Django 2.2.10 on 2020-08-05 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_auto_20200805_0328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(choices=[('S', 'Stripe'), ('B', 'Braintree'), ('P', 'Paypal'), ('C', 'Bitcoin')], max_length=1),
        ),
    ]