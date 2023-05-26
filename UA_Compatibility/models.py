from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Ty Hayes'

doc = """
An app for determining the suitability of the device a participant is accessing
this experiment from.  Records details about the device.

Requires django_user_agent middleware to populate most of the variables recorded.
"""


class Constants(BaseConstants):
    name_in_url = 'UA_Compatibility'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    device = models.StringField() #this field from django_user_agent was found to be unreliable and is not used
    browser = models.StringField() # Vendor and Version of the browser used to access the device (e.g. Chrome Mobile 109.0.0)
    os = models.StringField() # Operating system and version of the browser used to access the experiement (e.g. Android 13)
    ua_string = models.StringField() # User agent string taken from http headers sent when accessing the experiment
                                     # e.g. Mozilla/5.0 (Linux; Android 13; XQ-CC54) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36


