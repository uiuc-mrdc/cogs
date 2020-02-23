# Generated by Django 3.0.3 on 2020-02-23 05:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
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
                ('team_name', models.CharField(max_length=30)),
                ('school_name', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='GameParticipant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='team_management.Game')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='team_management.Team')),
            ],
        ),
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('multiplier', models.FloatField(default=1)),
                ('value', models.IntegerField(default=0)),
                ('deleted', models.BooleanField(default=False)),
                ('game_participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='team_management.GameParticipant')),
                ('scoring_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='team_management.ScoringType')),
            ],
        ),
    ]
