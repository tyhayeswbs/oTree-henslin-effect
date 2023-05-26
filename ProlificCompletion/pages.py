from otree.api import Currency as c, currency_range

from ._builtin import Page, WaitPage
from .models import *
import datetime

class Comments(Page):
    '''
    A page for free-text comments on the experiment.

    Note: this page not shown in this experiment (see page_sequence below)
    '''
    form_model = Player
    form_fields = ['feedback']

    def is_displayed(self):
        return True # see note

class StudyCompleted(Page):
    '''
    A page that shows the completion code (set this in the session config in sessions.py)

    The template for this page also contains signposting to support resources related to this study.
    '''
    def vars_for_template(self):
        return {
            'completion_code': self.session.config['completion_code'],
        }

page_sequence = [
    StudyCompleted,
]
