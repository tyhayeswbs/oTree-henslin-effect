from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


author = 'Ty Hayes'

doc = """
App for collecting demographic and gambling experience data
and administering the PGSI.

PGSI in this app is presented over multiple pages, optimized for
administering on a mobile device.

This app was also modified to be deployed as a qualifying survey,
by including "qualifying_survey = True" as an entry in the session
config dictionary.

"""


class Constants(BaseConstants):
    name_in_url = 'post_questionnaire'
    players_per_group = None
    num_rounds = 9
    responses = ["Never", "Sometimes", "Most of the time", "Almost always",]
    pgsi_categories = {"Non-problem gambler": {"min": 0, "max":0}, 
                      "Low-risk gambler": {"min": 1, "max": 2},
                      "Moderate-risk gambler": {"min": 3, "max": 7},
                      "Problem gambler": {"min": 8, "max": 27}
                      }
    demographic_categories = ["Craps Gambler", "Non-craps Gambler", "Non-gambler"]
    experimenter_pid = "YOURPID" # Prolific PID of experimenter for excluding any tests done
    experimental_sessions = [] #oTree codes for sessions that are part of the actual experiment



class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            pgsi_order = ['afford_to_lose',
                          'larger_amounts',
                          'win_back_losses',
                          'borrowed_money',
                          'subjective_gambling_problem',
                          'health_problems',
                          'external_gambling_problem',
                          'financial_problem',
                          'guilt',
                           ]
            for p in self.get_players():
                p.participant.vars['pgsi_order'] = pgsi_order 
                p.participant.save()


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.PositiveIntegerField(label="Age", blank=True, )  #participant's age
    age_prefer_not = models.BooleanField(label="Prefer not to disclose", blank=True, widget = widgets.CheckboxInput()) # participant would rather not disclose their age
    gender = models.CharField(label="Gender",widget=widgets.RadioSelect,
                              choices=['Male', 'Female', 'Non-binary', 'Other', 'Prefer not to Disclose']) #participant's gender
    gender_specifics = models.CharField(label="Please specify if you wish", blank=True) #free text entry for participant to self-define their gender identity
    
    afford_to_lose = models.StringField(widget=widgets.RadioSelect, 
                                 label = "Have you bet more than you could really afford to lose?",
                                 choices = Constants.responses,
                                ) #PGSI item
    larger_amounts = models.StringField(widget=widgets.RadioSelect, 
                                 label = "Have you needed to gamble with larger amounts of money to get the same feeling of excitement?",
                                 choices = Constants.responses,
                                )#PGSI item

    win_back_losses = models.StringField(widget=widgets.RadioSelect, 
                                 label = "When you gambled, did you go back another day to try to win back the money you lost?",
                                 choices = Constants.responses,
                                )#PGSI item

    borrowed_money = models.StringField(widget=widgets.RadioSelect, 
                                 label = "Have you borrowed money or sold anything to get money to gamble?",
                                 choices = Constants.responses,
                                )#PGSI item

    subjective_gambling_problem = models.StringField(widget=widgets.RadioSelect, 
                                 label = "Have you felt that you might have a problem with gambling?",
                                 choices = Constants.responses,
                                )#PGSI item

    health_problems = models.StringField(widget=widgets.RadioSelect, 
                                 label = "Has gambling caused you any health problems, including stress or anxiety?",
                                 choices = Constants.responses,
                                )#PGSI item

    external_gambling_problem = models.StringField(widget=widgets.RadioSelect, 
                                 label = "Have people criticised your betting or told you that you had a gambling problem,<br /> regardless of whether or not you thought it was true?",
                                 choices = Constants.responses,
                                )#PGSI item

    financial_problem = models.StringField(widget=widgets.RadioSelect, 
                                 label = "Has your gambling caused any financial problems for you or your household?",
                                 choices = Constants.responses,
                                )#PGSI item

    guilt = models.StringField(widget=widgets.RadioSelect, 
                                 label = "Have you felt guilty about the way you gamble or what happens when you gamble?",
                                 choices = Constants.responses,
                                )#PGSI item

    comments = models.TextField(label="Do you have any comments about the study?") #free text question for participants to comment on the study
    baccarat = models.BooleanField(blank=True, null=True) #gambling experience item
    bingo = models.BooleanField(blank=True, null=True) #gambling experience item
    blackjack = models.BooleanField(blank=True, null=True) #gambling experience item
    craps = models.BooleanField(blank=True, null=True) #gambling experience item
    lottery = models.BooleanField(blank=True, null=True) #gambling experience item
    pachinko = models.BooleanField(blank=True, null=True) #gambling experience item
    poker = models.BooleanField(blank=True, null=True) #gambling experience item
    sports_book = models.BooleanField(blank=True, null=True) #gambling experience item
    roulette = models.BooleanField(blank=True, null=True) #gambling experience item
    slots = models.BooleanField(blank=True, null=True) #gambling experience item
    video_poker = models.BooleanField(blank=True, null=True) #gambling experience item
    virtual_sports = models.BooleanField(blank=True, null=True) #gambling experience item
    none_above = models.BooleanField(blank=True, null=True) #gambling experience item

    @property
    def gambling_category(self):
        '''
        Derives classification of participant according to the preregistration
        '''
        if self.in_round(1).craps:
            return "Craps gambler"
        elif self.in_round(1).none_above:
            return "Non gambler"
        else:
            return "Other gambler"
    
    @property
    def pgsi_score(self):
        '''
        Calculates aggregate PGSI score according to Ferris & Wynne 2001
        '''
        try:
            if not self.in_round(1).none_above:
                pgsi_statements = ["afford_to_lose", "larger_amounts", "win_back_losses", "borrowed_money", "subjective_gambling_problem", "health_problems", "external_gambling_problem", "financial_problem", "guilt",]
                aggregate_score = sum([Constants.responses.index(getattr(self.in_round(pgsi_statements.index(field)+1),field)) for field in pgsi_statements])
                return aggregate_score
            else:
                return None
        except:
            return None
                


def custom_export(players):
    headers = ['participant_code', 'age','gender', 'gender_specifics', 'gambling_category', 'pgsi_score']
    yield headers
    for p in players:
        # only process final round players
        if p.round_number != Constants.num_rounds:
            continue
        # exclude incompletes as withdrawals
        if p.participant._index_in_pages < p.participant._max_page_index:
            continue
        # only include participants from the main experimental sessions (set in constants)
        if p.session.code not in Constants.experimental_sessions:
            continue
        # exclude data recorded when experimenter was testing
        if p.participant.label == Constants.researcher_pid: # remove experimenter's test data by id
            continue
        yield [p.participant.code, p.age, p.gender, p.gender_specifics, p.gambling_category, p.pgsi_score]

