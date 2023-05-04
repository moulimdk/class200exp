from os import environ

SESSION_CONFIGS = [
    dict(
        name='prisoners_dilemma',
        display_name = "Prisoner's Dilemma Game",
        app_sequence=['g1_PD'],
        num_demo_participants=2,
        payoffs=[[48,12],[50,25]],
    ),
    dict(
        name='bertrand',
        display_name = "Bertrand Market Game",
        app_sequence=['g2_bertrand'],
        num_demo_participants=2,
        mc = 2,
    ),
    dict(
        name='public_good_game',
        display_name = "Public Good Game",
        app_sequence=['g3_PGG'],
        num_demo_participants=2,
    ),
    dict(
        name='tragedy_common',
        display_name = "Tragedy of Commons Game",
        app_sequence=['g4_tragedy'],
        num_demo_participants=2,
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, 
    participation_fee=0.00, 
    doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '5130123912720'
