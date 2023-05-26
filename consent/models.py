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
    An app for displaying a participant information leaflet
    and recording consent to participate
"""


class Constants(BaseConstants):
    name_in_url = 'consent'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    consent = models.BooleanField(label="", choices=[[True,"I have read and understood the above and consent to take part in this study"],[False, "I do not wish to continue"]]) #participant's response to the consent question
