from otree.api import *
import settings
import random

author = "Mouli Modak"

doc = """
Experiment App for Tragedy of the Commons
"""

class C(BaseConstants):

    NAME_IN_URL = 'tragedy'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 5
    GROWTH = 1.2
    ENDOWMENT = 1200 

class Subsession(BaseSubsession):

    total_harvested = models.IntegerField(initial=0)
    total_available = models.FloatField(initial=0)
    remaining = models.FloatField(initial=0)
    continue_game = models.IntegerField(initial=1)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    
    myName = models.StringField()
    myAction = models.IntegerField(
       initial = 0, min=0, max=10, label="How many units of fish will you choose to harvest?"
    )
    myPayment = models.FloatField(initial=0)


## SUBMISSION METHODS

def creating_session(subsession: Subsession):

    players = subsession.get_players()
    random.shuffle(players)
    matrix = []
    matrix.append(players)
    subsession.set_group_matrix(matrix)
    if subsession.round_number == 1:
        subsession.total_available = C.ENDOWMENT


## GROUP METHODS

def result_update(group: Group):

    players = group.get_players()

    for p in players:
        group.subsession.total_harvested += p.myAction
    
    group.subsession.remaining = group.subsession.total_available - group.subsession.total_harvested
    
    if group.subsession.remaining <= 0:
        for nr in range(group.round_number+1, C.NUM_ROUNDS+1):
            group.subsession.in_round(nr).continue_game = 0
        for p in players:
            p.myPayment = round(p.myAction + (group.subsession.remaining*p.myAction/group.subsession.total_harvested),2)
    else:
        for p in players:
            p.myPayment = p.myAction

# PAGES

class P1_Instruction(Page):

    form_model = 'player'
    form_fields = ['myName']

    @staticmethod
    def vars_for_template(player: Player):

        dict_return = dict(
            total_endowment = C.ENDOWMENT,
            growth = C.GROWTH,
            num_periods = C.NUM_ROUNDS,
            next_endowment = C.GROWTH*400,
            # period = C.NUM_ROUNDS
        )

        return dict_return
    
    def is_displayed(player: Player):

        return player.round_number == 1


class P2_Experiment(Page):

    form_model = 'player'
    form_fields = ['myAction']

    @staticmethod
    def vars_for_template(player: Player):

        if player.round_number > 1:
            player.subsession.total_available = round(C.GROWTH*player.subsession.in_round(player.round_number-1).remaining,0)

        dict_return = dict(
            total_endowment = player.subsession.total_available,
            growth = C.GROWTH,
            period_number = player.round_number,
            num_periods = C.NUM_ROUNDS,
        )

        return dict_return
    
    def is_displayed(player: Player):

        return (player.round_number <= C.NUM_ROUNDS) & (player.subsession.continue_game == 1)
    

class P3_WaitingForAll(WaitPage):
    
    template_name = "g4_tragedy/templates/P3_WaitingForAll.html"

    after_all_players_arrive = result_update

    @staticmethod
    def vars_for_template(player: Player):

        dict_return = dict(
            myAction = player.myAction,
        )

        return dict_return

    def is_displayed(player: Player):
        
        return (player.round_number <= C.NUM_ROUNDS) & (player.subsession.continue_game == 1)
    

class P4_Results(Page):
    
    @staticmethod
    def vars_for_template(player: Player):

        dict_return = dict(
            myAction1 = player.in_round(1).myAction,
            harvest1 = player.subsession.in_round(1).total_harvested,
            available1 = player.subsession.in_round(1).total_available,
            payoff1 = player.in_round(1).myPayment,
            myAction2 = player.in_round(2).myAction,
            harvest2 = player.subsession.in_round(2).total_harvested,
            available2 = player.subsession.in_round(2).total_available,
            payoff2 = player.in_round(2).myPayment,
            myAction3 = player.in_round(3).myAction,
            harvest3 = player.subsession.in_round(3).total_harvested,
            available3 = player.subsession.in_round(3).total_available,
            payoff3 = player.in_round(3).myPayment,
            myAction4 = player.in_round(4).myAction,
            harvest4 = player.subsession.in_round(4).total_harvested,
            available4 = player.subsession.in_round(4).total_available,
            payoff4 = player.in_round(4).myPayment,
            myAction5 = player.in_round(5).myAction,
            harvest5 = player.subsession.in_round(5).total_harvested,
            available5 = player.subsession.in_round(5).total_available,
            payoff5 = player.in_round(5).myPayment,
            myPayoff = round(player.in_round(1).myPayment+player.in_round(2).myPayment+player.in_round(3).myPayment+player.in_round(4).myPayment+player.in_round(5).myPayment,2),
        )

        return dict_return
    
    def is_displayed(player: Player):
        
        return player.round_number == C.NUM_ROUNDS


page_sequence = [
                P1_Instruction,
                P2_Experiment,
                P3_WaitingForAll,
                P4_Results,
                ]