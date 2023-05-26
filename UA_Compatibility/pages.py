from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class CheckCompatibility(Page):
    '''
    Page that checks the device is compatible with the experiment

    Javascript in the template further contains specific functionality
    tests to check for 
        - accelerometer support in the browser
        - permissions for the experiment to access it
            - prompt/instructions how to allow access if not detected
    '''
    def vars_for_template(self):
        if not self.request.user_agent.is_mobile:
            return {'compatibility': False,
                    'mobile': False,
                    }
        elif not self.request.user_agent.is_touch_capable:
            return {'compatibility': False,
                    'mobile': self.request.user_agent.is_mobile,
                    'touch': False,}
        elif "firefox" in self.request.user_agent.browser.family.lower():
            return {'compatibility': False,
                    'firefox': True,
                    'mobile': self.request.user_agent.is_mobile,
                    'os': self.request.user_agent.os.family}
        else: 
            return {'compatibility': True}
    
    def before_next_page(self):
        browser = self.request.user_agent.browser
        os = self.request.user_agent.os
        self.player.browser = f"{browser.family} {browser.version_string}"
        self.player.os = f"{os.family} {os.version_string}"
        self.player.ua_string = self.request.META['HTTP_USER_AGENT']
        self.player.save()


page_sequence = [
    CheckCompatibility,
]
