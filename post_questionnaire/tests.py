from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):

    def play_round(self):
        
        submission = {}
        for field in ['afford_to_lose','larger_amounts','win_back_losses','borrowed_money',
                    'subjective_gambling_problem','health_problems','external_gambling_problem',
                    'financial_problem','guilt',]:
            submission[field] = random.choice(Constants.responses)

        yield pages.Questionnaire, submission
        yield pages.Demographics, {'age': 99, 'gender': 'Prefer Not to Disclose', 'gender_specifics': ""}
