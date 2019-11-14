# Generated by Django 2.2.7 on 2019-11-11 05:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ScoringType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('limit', models.IntegerField(default=0)),
                ('value', models.IntegerField()),
                ('extra_data', models.CharField(max_length=20)),
                ('input_group', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=100)),
                ('school_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='LiveScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(verbose_name='date published')),
                ('scoring_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='team_management.ScoringType')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='team_management.Team')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score1', models.IntegerField(default=0)),
                ('score2', models.IntegerField(default=0)),
                ('score3', models.IntegerField(default=0)),
                ('score4', models.IntegerField(default=0)),
                ('start_time', models.DateTimeField(verbose_name='date published')),
                ('finished', models.BooleanField(default=False)),
                ('special_name', models.CharField(default='', max_length=25)),
                ('team2', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='team2', to='team_management.Team')),
                ('team3', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='team3', to='team_management.Team')),
                ('team4', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='team4', to='team_management.Team')),
                ('teamOne', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='team1', to='team_management.Team')),
            ],
        ),
    ]