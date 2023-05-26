from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants




class DisableScreenRotation(Page):
    '''
    Page to encourage participant to disable automatic
    screen rotation/lock the screen orientation so the
    screen does not reorient during the task

    '''
    pass

class SoundLevels(Page):
    '''
    Page to give the participants an opportunity to 
    check they can hear the audible stimuli and 
    tune the volume for them.
    '''
    pass

class ReadyToStart(Page):
    '''
    Page immediately before the main experimental task begins
    with brief troubleshooting advice and encouraging care
    to hold phone tightly
    '''
    pass


page_sequence = [DisableScreenRotation, SoundLevels, ReadyToStart,]
