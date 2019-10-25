"""Class for making arbitrator object"""
import random


class Arbitrator:
    """Class for making arbitrator"""
    def __init__(self, this_bbcon, bbcon_det):
        self.bbcon = this_bbcon
        self.det_choose_action = bbcon_det  # boolean used to let bbcon decide
        # if it wants to use deterministic choose_action

    def choose_action(self):
        """Calls deterministic og stochastic choose_action
         depending on value of det_choose_action"""
        print("entered Choose_action")
        if self.det_choose_action:
            self.choose_action_deterministic()
        else:
            self.choose_action_stochastic()

    def choose_action_deterministic(self):
        """Access all active behaviors from bbcon and chooses the behavior
        with largest weight. Returns motor recommendations of this behavior"""
        active_behaviors = self.bbcon.active_behaviors
        print(active_behaviors[0])
        winner_behavior = active_behaviors[0]
        max_weight = winner_behavior.get_weight()
        for this_behavior in active_behaviors:
            if this_behavior.get_weight() > max_weight:  # if there is a behavior with larger weight
                winner_behavior = this_behavior
                max_weight = this_behavior.get_weight()

        return [winner_behavior.get_motor_recs(), winner_behavior.get_halt_request()]
        # return motor recommendation and halt_request of behavior with largest weight

    def choose_action_stochastic(self):
        """Access all active behaviors from bbcon and chooses the behavior
        with largest weight. Returns motor recommendations of this behavior"""
        num = 0
        # ex: {B1: [0, 0.8], B2: [0.8, 1.3], B3: [1.3, 2.0]}
        dict_behaviors = {}
        active_behaviors = self.bbcon.active_behaviors

        # Fill dictionary with behavior-objects and their weight range
        for this_behavior in active_behaviors:
            weight = this_behavior.get_weight()
            dict_behaviors[this_behavior] = [num, num + weight]
            num += weight

        random_num = random.randint(0, num)
        winner_behavior = None

        # Iterate through dictionary and sets winner_behavior
        # equal the one with weight range that covers r
        for key, value in dict_behaviors.items():
            if value[1] < random_num:  # makes sure r matches with largest possible weight range
                winner_behavior = key
        return winner_behavior.get_motor_recs(), winner_behavior.get_halt_request()
        # return motor recommendation and halt_request of behavior with weight
        # that covers r
