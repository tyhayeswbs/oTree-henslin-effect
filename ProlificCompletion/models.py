from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

author = 'Ty Hayes'

doc = """
A barebones library app for recording a participant's id
from the recruitment platform Prolific.co
"""



class Constants(BaseConstants):
    name_in_url = 'complete'
    players_per_group = None
    num_rounds = 1

    time_format = "%Y-%m-%d %H:%M"



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    feedback = models.TextField(label="Comments" )  # a text area for free-text comments
