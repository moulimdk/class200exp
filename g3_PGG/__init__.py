from otree.api import *
import settings
import random

author = "Mouli Modak"

doc = """
Experiment App for Unconditional Public Good Games
"""

class C(BaseConstants):

    NAME_IN_URL = 'pgg'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    MULTIPLIER = 1.6
    ENDOWMENT = 4

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    
    myName = models.StringField()
    myAction = models.IntegerField(
        min=0, max=C.ENDOWMENT, label="How much will you contribute?"
    )
    other1Action = models.IntegerField()
    other2Action = models.IntegerField()
    myPayment = models.FloatField(initial=0)
    other1Payment = models.FloatField(initial=0)
    other2Payment = models.FloatField(initial=0)
    pge = models.FloatField(initial=0)


## SUBMISSION METHODS

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

        player = unmatched[0]

        if len(unmatched) > 2:

            print(len(unmatched))

            other_number = random.sample(range(1, len(unmatched)),2)
            other1 = unmatched[other_number[0]]
            other2 = unmatched[other_number[1]]

            player.other1Action = other1.myAction
            player.other2Action = other2.myAction
            other1.other1Action = player.myAction
            other2.other1Action = player.myAction
            other1.other2Action = other2.myAction
            other2.other2Action = other1.myAction

            player.pge = round((C.MULTIPLIER)*(player.myAction+player.other1Action+player.other2Action)/3,1)
            other1.pge = round((C.MULTIPLIER)*(player.myAction+player.other1Action+player.other2Action)/3,1)
            other2.pge = round((C.MULTIPLIER)*(player.myAction+player.other1Action+player.other2Action)/3,1)

            player.myPayment = (C.ENDOWMENT - player.myAction) + player.pge
            other1.myPayment = (C.ENDOWMENT - other1.myAction) + player.pge
            other2.myPayment = (C.ENDOWMENT - other2.myAction) + player.pge

            player.other1Payment = other1.myPayment
            player.other2Payment = other2.myPayment
            other1.other1Payment = player.myPayment
            other1.other2Payment = other2.myPayment
            other2.other1Payment = player.myPayment
            other2.other2Payment = other1.myPayment
            
            player.payoff = player.myPayment
            other1.payoff = other1.myPayment
            other2.payoff = other2.myPayment

            matched.append(player)
            matched.append(other1)
            matched.append(other2)

            unmatched.remove(player)
            unmatched.remove(other1)
            unmatched.remove(other2)

        elif len(unmatched) == 2:

            other1 = unmatched[1]

            player.other1Action = other1.myAction
            player.other2Action = random.randint(0, C.ENDOWMENT)
            other1.other1Action = player.myAction
            other1.other2Action = player.other2Action

            player.pge = round((C.MULTIPLIER)*(player.myAction+player.other1Action+player.other2Action)/3,1)
            other1.pge = round((C.MULTIPLIER)*(player.myAction+player.other1Action+player.other2Action)/3,1)

            player.myPayment = (C.ENDOWMENT - player.myAction) + player.pge
            other1.myPayment = (C.ENDOWMENT - other1.myAction) + player.pge
            other2myPayment = (C.ENDOWMENT - player.other2Action) + player.pge

            player.other1Payment = other1.myPayment
            player.other2Payment = other2myPayment
            other1.other1Payment = player.myPayment
            other1.other2Payment = other2myPayment

            player.payoff = player.myPayment
            other1.payoff = other1.myPayment

            matched.append(player)
            matched.append(other1)
            unmatched.remove(player)
            unmatched.remove(other1)

        elif len(unmatched) == 1:

            player.other1Action = random.randint(0, C.ENDOWMENT)
            player.other2Action = random.randint(0, C.ENDOWMENT)

            player.pge = round((C.MULTIPLIER)*(player.myAction+player.other1Action+player.other2Action)/3,1)

            player.myPayment = (C.ENDOWMENT - player.myAction) + player.pge
            other1myPayment = (C.ENDOWMENT - player.other1Action) + player.pge
            other2myPayment = (C.ENDOWMENT - player.other2Action) + player.pge

            player.other1Payment = other1myPayment
            player.other2Payment = other2myPayment

            player.payoff = player.myPayment

            matched.append(player)
            unmatched.remove(player)


# PAGES

class P1_Instruction(Page):

    form_model = 'player'
    form_fields = ['myName', 'myAction']

    @staticmethod
    def vars_for_template(player: Player):

        dict_return = dict(
            group_number = 2,
            multiplier = C.MULTIPLIER,
            endowment = C.ENDOWMENT,
            pgeTotal = round(3*C.MULTIPLIER, 1),
            example = C.ENDOWMENT - 1 + C.MULTIPLIER
        )

        return dict_return
    
    def is_displayed(player: Player):

        return player.round_number <= C.NUM_ROUNDS  


# class P2_Experiment(Page):

#     form_model = 'player'
#     form_fields = ['myAction']

#     @staticmethod
#     def vars_for_template(player: Player):

#         dict_return = dict(
#             group_number = 2,
#             multiplier = C.MULTIPLIER,
#             endowment = C.ENDOWMENT,
            
#         )

#         return dict_return
    
#     def is_displayed(player: Player):

#         return player.round_number == C.NUM_ROUNDS
    

class P3_WaitingForAll(WaitPage):
    
    template_name = "g3_PGG/templates/P3_WaitingForAll.html"

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
            total_pge = player.myAction+player.other1Action+player.other2Action,
            return_pge = round(3*player.pge,1),
            pge = player.pge,
            other1Action = player.other1Action,
            other1Payoff = player.other1Payment,
            other2Action = player.other2Action,
            other2Payoff = player.other2Payment,
        )

        return dict_return
    
    def is_displayed(player: Player):
        
        return player.round_number <= C.NUM_ROUNDS


page_sequence = [
                P1_Instruction,
                # P2_Experiment,
                P3_WaitingForAll,
                P4_Results,
                ]