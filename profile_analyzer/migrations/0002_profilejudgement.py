# Generated by Django 2.2.10 on 2020-12-09 21:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profile_analyzer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileJudgement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('decision', models.BooleanField(default=False)),
                ('date_analyzed', models.DateTimeField(auto_now_add=True)),
                ('profile_analysis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profile_analyzer.ProfileAnalysis')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]