from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Ty Hayes'

doc = """
A barebones app for recording a participant's id
from the recruitment platform Prolific.co
"""


class Constants(BaseConstants):
    name_in_url = 'Prolific'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    ProlificID = models.StringField( 
        label="My Prolific ID is",
        )  # The participant's ID
