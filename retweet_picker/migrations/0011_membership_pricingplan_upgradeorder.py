# Generated by Django 2.2.10 on 2020-10-24 04:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_orderitem_status'),
        ('retweet_picker', '0010_auto_20201013_0441'),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(default=0)),
                ('plan', models.CharField(choices=[('F', 'Free'), ('B', 'Basic'), ('P', 'Pro')], default='F', max_length=1)),
                ('paid_month', models.IntegerField(default=0)),
                ('paid_time', models.DateTimeField(null=True)),
                ('end_time', models.DateTimeField(null=True)),
                ('done_count', models.IntegerField(default=0)),
                ('done_month', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='PricingPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.CharField(choices=[('F', 'Free'), ('B', 'Basic'), ('P', 'Pro')], max_length=1)),
                ('label', models.CharField(blank=True, max_length=200)),
                ('price', models.IntegerField(default=1)),
                ('limit_times', models.IntegerField(default=2)),
                ('limit_count', models.IntegerField(default=10000000)),
            ],
            options={
                'ordering': ['price'],
            },
        ),
        migrations.CreateModel(
            name='Upgradeorder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(default=0)),
                ('reason', models.CharField(blank=True, max_length=50, null=True)),
                ('amount', models.IntegerField(default=0)),
                ('months', models.IntegerField(default=0)),
                ('upgradeto', models.CharField(choices=[('F', 'Free'), ('B', 'Basic'), ('P', 'Pro')], default='B', max_length=1)),
                ('gwid', models.IntegerField(default=0)),
                ('payment_status', models.CharField(choices=[('W', 'Waiting'), ('P', 'Pending'), ('C', 'Complete')], default='W', max_length=1)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('payment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Payment')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]