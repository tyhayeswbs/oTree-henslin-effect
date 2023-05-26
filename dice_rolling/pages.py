from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class NewBlock(Page):
    '''
    page that draws participant attention to the new target
    '''
    def is_displayed(self):
        return self.round_number % Constants.trials_per_target == 1

class Trial(Page):
    '''
    main trial page - crucial data is recorded via live_method
    '''
    form_model = 'player'
    form_fields = ['final_die_z', 'animation']
    live_method = 'live_method'
    def before_next_page(self):
        self.player.set_payoff()

page_sequence = [NewBlock, Trial]
