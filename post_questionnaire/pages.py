from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import datetime, pytz
from pprint import pprint

class Questionnaire(Page):
    '''
    Single page version of PGSI (not used in this experiment - see page_sequence below)
    '''
    form_model = 'player'
    form_fields = [
                   'afford_to_lose','larger_amounts','win_back_losses','borrowed_money',
                    'subjective_gambling_problem','health_problems','external_gambling_problem',
                    'financial_problem','guilt',] 

    def is_displayed(self):
        return self.session.config['show_pgsi']

class GamblingExperience(Page):
    '''
    Page to record participant experience with each of the list of gambling games
    '''
    form_model = 'player'
    form_fields = ['baccarat','blackjack','bingo','craps','lottery','pachinko','poker', 'sports_book','roulette','slots','video_poker','virtual_sports','none_above']

    def error_message(self, values):
        selected_values = [item for item in values if values[item] is not None]
        if len(selected_values) == 0:
            return "You have not selected any responses.  If you have no experience with any of the listed games, please select \"None of the above\""
        if 'none_above' in selected_values:
            if len(selected_values) > 1:
                return f"You have chosen \"None of the above\" in addition to {len(selected_values) -1} other answer{'s' if len(selected_values) > 2 else ''}. Please check your responses."

    def is_displayed(self):
        return self.round_number == 1


class PGSI(Page):
    '''
    Page to record participant responses to items from the PSGI.
    '''
    form_model = 'player'
    def get_form_fields(self):
        '''
        Select the item from the list saved into the participant model
        on creating_session by indexing into it according to round_number
        '''
        return [self.participant.vars['pgsi_order'][self.round_number -1]]

    #def is_displayed(self):
    #    return self.session.config['show_pgsi']

    def is_displayed(self):
        ''' 
        don't display PGSI to participants without gambling experience
        '''
        return not self.player.in_round(1).none_above
    
class Demographics(Page):
    '''
    Page to collect participant demographics
    '''
    form_model = 'player'
    form_fields = ['age',
                   'age_prefer_not',
                   'gender',
                   'gender_specifics',]

    def is_displayed(self):
        '''
        only show in the final round
        '''
        return self.round_number == Constants.num_rounds

    def error_message(self, values):
        if not ( values['age'] or values['age_prefer_not']):
            return "If you do not wish to provide your age, please check the 'prefer not to disclose' box"
        if values['age'] and values['age_prefer_not']:
            return "If you do not wish to provide your age, please clear the 'age' textbox.  Otherwise, please uncheck the 'prefer not to disclose' box for the age question."


class Comments(Page):
    '''
    Page for any free text comments the participant has at the end of the experiment
    '''
    form_model = 'player'
    form_fields = ['comments']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class Introduction(Page):
    '''
    Brief introductory page for deployment of this app as a qualifying survey
    (only shows Introduction, GamblingExperience and ProlificCompletion)
    '''
    def is_displayed(self):
        if self.round_number != 1:
            return False
        return self.session.config.get('qualifying_survey', False)


class ProlificCompletion(Page):
    '''
    Final page including prolific completion link (set in session config)
    for deployment of this app as a qualifying survey
    (only shows Introduction, GamblingExperience and ProlificCompletion)

    Note: this page does not contain a next button - participants are directed
    to the prolific completion page and do not continue through the rest of the app
    '''
    def vars_for_template(self):
        return {'completion_code': self.session.config.get('prolific_completion_code', 'XXXXXX') }

    def is_displayed(self):
        if self.round_number != 1:
            return False
        return self.session.config.get('qualifying_survey', False)

page_sequence = [
    #Queostionnaire,
    Introduction,
    GamblingExperience,
    ProlificCompletion,
    PGSI,
    Demographics,
    Comments,
]
