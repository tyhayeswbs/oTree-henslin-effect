from otree.api import Currency as c, currency_range

from . import pages
from ._builtin import Bot
from .models import Constants
import datetime

class PlayerBot(Bot):

    def play_round(self):
        #if datetime.datetime.now() < datetime.datetime.strptime(self.session.config['pilot_end_time'],
        #                                                        Constants.time_format):
        #    yield (pages.PilotFeedback, {'feedback': 'yada yada'})
        yield (pages.StudyCompleted)
