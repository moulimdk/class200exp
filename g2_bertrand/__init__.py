from otree.api import *
import settings
import random

author = "Mouli Modak"

doc = """
Experiment App for Symmetric Bertrand Competition.
"""

class C(BaseConstants):

    NAME_IN_URL = 'G2_Bertrand'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    MC = settings.SESSION_CONFIGS[1].get("mc")

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    
    myName = models.StringField()
    myAction = models.IntegerField(
        choices=[i for i in range(11)],
        widget=widgets.RadioSelect
    )
    otherAction = models.IntegerField()
    myPayment = models.FloatField(initial=0)
    otherPayment = models.FloatField(initial=0)


## Subsession method

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
            # print("Other=",other)
            player.otherAction = other.myAction
            other.otherAction = player.myAction
            if player.myAction < player.otherAction:
                quantity = 10 - player.myAction
                player.myPayment = (player.myAction - C.MC)*quantity
                other.myPayment = 0
            elif player.myAction > player.otherAction:
                quantity = 10 - player.otherAction
                other.myPayment = (other.myAction - C.MC)*quantity
                player.myPayment = 0
            else:
                quantity = 10 - player.myAction
                other.myPayment = (other.myAction - C.MC)*(quantity/2)
                player.myPayment = (player.myAction - C.MC)*(quantity/2)
            
            player.otherPayment = other.myPayment
            other.otherPayment = player.myPayment
            player.payoff = player.myPayment
            other.payoff = other.myPayment

            matched.append(player)
            matched.append(other)
            # print("Unmatched 1 =", unmatched)
            unmatched.remove(player)
            # print("Unmatched 2 =", unmatched)
            unmatched.remove(other)
            # print("Unmatched 3 =", unmatched)
        else:
            player.otherAction = random.randint(0, 10)
            if player.myAction < player.otherAction:
                quantity = 10 - player.myAction
                player.myPayment = (player.myAction - C.MC)*quantity
                player.otherPayment = 0
            elif player.myAction > player.otherAction:
                quantity = 10 - player.otherAction
                player.otherPayment = (player.otherAction - C.MC)*quantity
                player.myPayment = 0
            else:
                quantity = 10 - player.myAction
                player.otherPayment = (player.myAction - C.MC)*(quantity/2)
                player.myPayment = (player.myAction - C.MC)*(quantity/2)
            player.payoff = player.myPayment

            matched.append(player)
            unmatched.remove(player)

# PAGES

class P1_Instruction(Page):

    form_model = 'player'
    form_fields = ['myName']

    @staticmethod
    def vars_for_template(player: Player):

        dict_return = {}

        for p1 in range(11):
            for p2 in range(p1,11):

                if p1 < p2:
                    dict_label_1 = "P_{}{}".format(p1,p2)
                    dict_label_2 = "P_{}{}".format(p2,p1)
                    quantity = 10 - p1
                    dict_return[dict_label_1] = (p1 - C.MC)*quantity
                    dict_return[dict_label_2] = 0
                else:
                    dict_label = "P_{}{}".format(p1,p2)
                    quantity = 10 - p1
                    dict_return[dict_label] = (p1 - C.MC)*(quantity/2)

        return dict_return
    
    def is_displayed(player: Player):

        return player.round_number == 1 

class P2_Experiment(Page):

    form_model = 'player'
    form_fields = ['myAction']

    @staticmethod
    def vars_for_template(player: Player):

        dict_return = {}

        for p1 in range(11):
            for p2 in range(p1,11):

                if p1 < p2:
                    dict_label_1 = "P_{}{}".format(p1,p2)
                    dict_label_2 = "P_{}{}".format(p2,p1)
                    quantity = 10 - p1
                    dict_return[dict_label_1] = (p1 - C.MC)*quantity
                    dict_return[dict_label_2] = 0
                else:
                    dict_label = "P_{}{}".format(p1,p2)
                    quantity = 10 - p1
                    dict_return[dict_label] = (p1 - C.MC)*(quantity/2)

        return dict_return
    
    def is_displayed(player: Player):

        return player.round_number == C.NUM_ROUNDS


class P3_WaitingForAll(WaitPage):
    
    template_name = "g2_bertrand/templates/P3_WaitingForAll.html"

    after_all_players_arrive = result_update

    @staticmethod
    def vars_for_template(player: Player):

        dict_return = dict(
            myAction = player.myAction,
        )

        return dict_return

    def is_displayed(player: Player):
        
        return player.round_number <= C.NUM_ROUNDS


class P4_Results(Page):
    
    @staticmethod
    def vars_for_template(player: Player):

        dict_return = dict(
            myAction = player.myAction,
            myPayoff = player.myPayment,
            otherAction = player.otherAction,
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
