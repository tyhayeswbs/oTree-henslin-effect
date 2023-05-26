from os import environ
try:
    from secrets import DATABASE_URL, ADMIN_PASSWORD
    environ['DATABASE_URL'] = DATABASE_URL
    environ['OTREE_ADMIN_PASSWORD'] = ADMIN_PASSWORD
    DEBUG = False
except: 
    environ['OTREE_ADMIN_PASSWORD'] = "demo"

SESSION_CONFIGS = [
     dict(
        name='dice_rolling_no_pgsi',
        display_name="Full Dice Rolling Pilot (pgsi conditional on experience question)",
        num_demo_participants=1,
        app_sequence=['consent', 'UA_Compatibility','ProlificID', 'instructions', 'calibration', 'dice_rolling', 'post_questionnaire','ProlificCompletion'],
        button_before_play_sim = True,
        render_shadows = True,
        use_textures = True,
        use_prerecorded_simulations = True,
        completion_code="C12T7HTZ",
     ),
     dict(
        name='qualification_survey',
        display_name="Qualification Survey",
        num_demo_participants=1,
        app_sequence=['post_questionnaire'],
        show_pgsi = False,
        prolific_completion_code="XXXXXX",
        qualifying_survey = True,
     ),]


# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=3.80, doc=""
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')
environ['OTREE_AUTH_LEVEL'] = "DEMO"

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = 'k5pi7fno7w7mg-kn8_+=%k7ov(*&#z8nk!olm9tyw8px2@l5*o'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

MIDDLEWARE = [
    # Simplified static file serving.
    # https://warehouse.python.org/project/whitenoise/
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    ]
