# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import otree_save_the_change.decorators
import otree.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('otree', '0024_auto_20170828_0419'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('id_in_subsession', otree.db.models.PositiveIntegerField(null=True, db_index=True)),
                ('round_number', otree.db.models.PositiveIntegerField(null=True, db_index=True)),
                ('session', models.ForeignKey(related_name='prolificid_group', to='otree.Session')),
            ],
            options={
                'db_table': 'ProlificID_group',
            },
            bases=(otree_save_the_change.decorators.STCMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('id_in_group', otree.db.models.PositiveIntegerField(null=True, db_index=True)),
                ('_payoff', otree.db.models.CurrencyField(null=True, default=0, max_digits=12)),
                ('round_number', otree.db.models.PositiveIntegerField(null=True, db_index=True)),
                ('_group_by_arrival_time_arrived', otree.db.models.BooleanField(default=False, choices=[(True, 'Yes'), (False, 'No')])),
                ('_group_by_arrival_time_grouped', otree.db.models.BooleanField(default=False, choices=[(True, 'Yes'), (False, 'No')])),
                ('_group_by_arrival_time_timestamp', otree.db.models.FloatField(null=True)),
                ('ProlificID', otree.db.models.CharField(verbose_name='My Prolific ID is', max_length=80, null=True)),
                ('group', models.ForeignKey(null=True, to='ProlificID.Group')),
                ('participant', models.ForeignKey(related_name='prolificid_player', to='otree.Participant')),
                ('session', models.ForeignKey(related_name='prolificid_player', to='otree.Session')),
            ],
            options={
                'db_table': 'ProlificID_player',
            },
            bases=(otree_save_the_change.decorators.STCMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Subsession',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('round_number', otree.db.models.PositiveIntegerField(null=True, db_index=True)),
                ('session', models.ForeignKey(null=True, related_name='prolificid_subsession', to='otree.Session')),
            ],
            options={
                'db_table': 'ProlificID_subsession',
            },
            bases=(otree_save_the_change.decorators.STCMixin, models.Model),
        ),
        migrations.AddField(
            model_name='player',
            name='subsession',
            field=models.ForeignKey(to='ProlificID.Subsession'),
        ),
        migrations.AddField(
            model_name='group',
            name='subsession',
            field=models.ForeignKey(to='ProlificID.Subsession'),
        ),
    ]
