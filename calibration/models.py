from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)


author = 'Ty Hayes'

doc = """

An app to help participants configure their phone for the smoothest
experience with the experiment.  

This app is just a modular container for technical instruction pages
and records no data.

"""


class Constants(BaseConstants):
    name_in_url = 'calibration'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass
