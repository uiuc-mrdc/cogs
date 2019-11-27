# Generated by Django 2.2.7 on 2019-11-27 23:33

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
                ('score1', models.IntegerField(default=0)),
                ('score2', models.IntegerField(default=0)),
                ('score3', models.IntegerField(default=0)),
                ('score4', models.IntegerField(default=0)),
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
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='team_management.Team')),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='team1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='team1', to='team_management.Team'),
        ),
        migrations.AddField(
            model_name='game',
            name='team2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='team2', to='team_management.Team'),
        ),
        migrations.AddField(
            model_name='game',
            name='team3',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='team3', to='team_management.Team'),
        ),
        migrations.AddField(
            model_name='game',
            name='team4',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='team4', to='team_management.Team'),
        ),
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('multiplier', models.FloatField(default=1)),
                ('upDown', models.BooleanField(default=1)),
                ('deleted', models.BooleanField(default=False)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='team_management.Game')),
                ('scoring_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='team_management.ScoringType')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='team_management.Team')),
            ],
        ),
    ]
