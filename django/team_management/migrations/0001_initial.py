# Generated by Django 3.0.3 on 2020-03-05 06:05

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(default=datetime.datetime(2020, 9, 20, 6, 5, 49, 483073, tzinfo=utc))),
                ('end_time', models.DateTimeField(default=datetime.datetime(2020, 9, 21, 6, 5, 49, 483149, tzinfo=utc))),
                ('finished', models.BooleanField(default=False)),
                ('special_name', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ScoringType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('limit', models.IntegerField(default=0)),
                ('value', models.IntegerField()),
                ('extra_data', models.CharField(max_length=10)),
                ('input_style', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=70)),
                ('school_name', models.CharField(max_length=500)),
                ('abbr', models.CharField(default='', max_length=8)),
                ('capt_name', models.CharField(max_length=25)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=15)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='team_management.Team')),
            ],
        ),
        migrations.CreateModel(
            name='GameParticipant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('color', models.CharField(default='gray', max_length=10)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='team_management.Game')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='team_management.Team')),
            ],
        ),
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=datetime.datetime(2020, 3, 5, 6, 5, 49, 484198, tzinfo=utc))),
                ('multiplier', models.FloatField(default=1)),
                ('value', models.IntegerField(default=0)),
                ('deleted', models.BooleanField(default=False)),
                ('game_participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='team_management.GameParticipant')),
                ('scoring_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='team_management.ScoringType')),
            ],
        ),
    ]
