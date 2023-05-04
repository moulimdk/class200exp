from otree.api import *
import settings
import random

author = "Mouli Modak"

doc = """
Experiment App for Prisoner's Dilemma Game
"""

class C(BaseConstants):

    NAME_IN_URL = 'G1_PD'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    PAYOFFS = settings.SESSION_CONFIGS[0].get("payoffs")


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    myName = models.StringField()
    myAction = models.IntegerField()
    otherAction = models.IntegerField()
    myPayment = models.CurrencyField(initial=0)
    otherPayment = models.CurrencyField(initial=0)


## SUBSESSION METHODS
def creating_session(subsession: Subsession):

    players = subsession.get_players()
    random.shuffle(players)
    matrix = []
    matrix.append(players)
    subsession.set_group_matrix(matrix)


## GROUP METHODS

def result_update(group: Group):

    players = group.get_players()

    unmatched = players
    matched = []

    while len(unmatched) > 0:
        player = players[0]
        if len(unmatched) > 1:
            other_number = random.randint(1, len(unmatched)-1)
            other = unmatched[other_number]
            # print(other)
            player.otherAction = other.myAction
            other.otherAction = player.myAction
            player.myPayment = C.PAYOFFS[player.myAction][player.otherAction]
            other.myPayment = C.PAYOFFS[other.myAction][other.otherAction]
            player.otherPayment = other.myPayment
            other.otherPayment = player.myPayment
            player.payoff = player.myPayment
            other.payoff = other.myPayment

            matched.append(player)
            matched.append(other)
            # print(unmatched)
            unmatched.remove(player)
            # print(unmatched)
            unmatched.remove(other)
            # print(unmatched)
        else:
            player.otherAction = random.randint(0, 1)
            player.myPayment = C.PAYOFFS[player.myAction][player.otherAction]
            player.otherPayment = C.PAYOFFS[player.otherAction][player.myAction]
            player.payoff = player.myPayment

            matched.append(player)
            unmatched.remove(player)


# PAGES

class P1_Instruction(Page):

    form_model = 'player'
    form_fields = ['myName']

    @staticmethod
    def vars_for_template(player: Player):

        dict_return = dict(
            CC_1 = C.PAYOFFS[0][0],
            CC_2 = C.PAYOFFS[0][0],
            CD_1 = C.PAYOFFS[0][1],
            CD_2 = C.PAYOFFS[1][0],
            DC_1 = C.PAYOFFS[1][0],
            DC_2 = C.PAYOFFS[0][1],
            DD_1 = C.PAYOFFS[1][1],
            DD_2 = C.PAYOFFS[1][1],
        )

        return dict_return
    
    def is_displayed(player: Player):

        return player.round_number == 1    
    

class P2_Experiment(Page):

    form_model = 'player'
    form_fields = ['myAction']

    @staticmethod
    def vars_for_template(player: Player):

        dict_return = dict(
            CC_1 = C.PAYOFFS[0][0],
            CC_2 = C.PAYOFFS[0][0],
            CD_1 = C.PAYOFFS[0][1],
            CD_2 = C.PAYOFFS[1][0],
            DC_1 = C.PAYOFFS[1][0],
            DC_2 = C.PAYOFFS[0][1],
            DD_1 = C.PAYOFFS[1][1],
            DD_2 = C.PAYOFFS[1][1],
        )

        return dict_return
    
    def is_displayed(player: Player):

        return player.round_number == C.NUM_ROUNDS


class P3_WaitingForAll(WaitPage):
    
    template_name = "g1_PD/templates/P3_WaitingForAll.html"

    after_all_players_arrive = result_update

    @staticmethod
    def vars_for_template(player: Player):

        actions = ["Cooperation", "Defection"]

        dict_return = dict(
            myAction = actions[player.myAction],
        )

        return dict_return

    def is_displayed(player: Player):
        
        return player.round_number <= C.NUM_ROUNDS


class P4_Results(Page):
    
    @staticmethod
    def vars_for_template(player: Player):

        actions = ["Cooperation", "Defection"]

        dict_return = dict(
            myAction = actions[player.myAction],
            myPayoff = player.myPayment,
            otherAction = actions[player.otherAction],
            otherPayoff = player.otherPayment,
        )

        return dict_return
    
    def is_displayed(player: Player):
        
        return player.round_number <= C.NUM_ROUNDS


page_sequence = [
                P1_Instruction,
                P2_Experiment,
                P3_WaitingForAll,
                P4_Results,
                ]
