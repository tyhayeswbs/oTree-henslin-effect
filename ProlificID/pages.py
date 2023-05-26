from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import *


class ProlificID(Page):
    '''
    A page with a text box for participant's to enter
    their Prolific Participant ID
    '''
    form_model = Player
    form_fields = ['ProlificID']


page_sequence = [
    ProlificID
]
