from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Overview(Page):
    pass

class Instructions1(Page):
    pass

class Instructions2(Page):
    pass

class Instructions3(Page):
    pass

class Instructions4(Page):
    pass

class Instructions5(Page):
    pass

class Instructions6(Page):
    pass

class Instructions7(Page):
    pass

page_sequence = [Overview, 
                Instructions1,
                Instructions2,
                Instructions3,
                Instructions4,
                Instructions5,
                Instructions6,
                Instructions7,
                ]
