from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class PIL(Page):
    '''
    Page to display the participant information leaflet with integrated
    question for the consent
    '''
    form_model = 'player'
    form_fields = ['consent']

class NoConsent(Page):
    '''
    Page to intercept any non-consents and disallow continuing with the
    rest of the experiment
    '''
    def is_displayed(self):
        return not (self.player.consent == True)


page_sequence = [
                PIL,
                NoConsent
                ]
