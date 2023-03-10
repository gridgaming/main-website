# Generated by Django 2.2.10 on 2020-06-02 20:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20200602_1642'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRoles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_type', models.CharField(default='New User', max_length=100)),
                ('quantifier', models.FloatField()),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='account_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.UserRoles'),
        ),
    ]
