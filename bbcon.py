"""Behavior-based controller. Called by robot at each timestep to determine its next move"""
from time import sleep
from zumo_button import ZumoButton
import arbitrator



class Bbcon:
    """Class for making Behavior-Based Controller"""
    def __init__(self):
        """initialize controller-object. One object per robot -> initialized one time at start"""
        self.behaviors = []
        self.active_behaviors = []
        self.inactive_behaviors = []
        self.sensobs = []
        self.motobs = []
        self.arbitrator = arbitrator(self)
        self.current_timestep = 0
        # self.robot = None

        # One instance per robot -> behaviors, sensobs and motobs are added at initialization

        # Add all behaviors to BBCON:
        # self.add_behavior(className()) wander_randomly?
        # self.add_behavior(className()) keep_in_area?
        # self.add_behavior(className()) avoid_collision?
        # self.add_behavior(className()) take_image?

        # Add all sensobs to BBCON:
        for this_behavior in self.behaviors:
            for this_sensob in this_behavior.sensobs:
                if this_sensob not in self.sensobs:  # behaviors use same sensob -> only add once
                    self.add_sensob(this_sensob)

        # Add motobs
        # ....

    def add_behavior(self, new_behavior):
        """append a newly-created behavior object to behaviors list"""
        self.behaviors.append(new_behavior)

    def add_sensob(self, new_sensob):
        """append a newly-created sensob object to sensobs list"""
        self.sensobs.append(new_sensob)

    def activate_behavior(self, existing_behavior):
        """add an existing behavior onto the active-behaviors list"""
        if existing_behavior not in self.active_behaviors:
            self.active_behaviors.append(existing_behavior)

    def deactivate_behavior(self, existing_behavior):
        """remove an existing behavior from the active-behaviors list"""
        if existing_behavior in self.active_behaviors:
            self.active_behaviors.pop(existing_behavior)

    def run_one_timestep(self):
        """method for core BBCON activity"""

        # Update all sensobs:
        for this_sensob in self.sensobs:  # sensobs contains no duplicates because of the adding-process
            this_sensob.update()  # sensob fetches relevant sensor values (once per timestep)

        # Update all behaviors:
        for this_behavior in self.behaviors:
            this_behavior.update()

        # Invoke arbitrator:
        motor_rec = self.arbitrator.choose_action()[0]  # returns (motor_rec, half_request)

        # Update motobs by giving motor recommendations:
        for this_motob in self.motobs:
            this_motob.update(motor_rec)

        # Wait:
        sleep(0.5)

        # Reset the sensobs:
        for this_sensob in self.sensobs:
            this_sensob.reset()


def main():
    """main-method for starting process"""
    bbcon = Bbcon()
    state = True
    ZumoButton().wait_for_press()  # place Zumo in waiting-loop until button is pressed
    while state:
        bbcon.run_one_timestep()


if __name__ == '__main__':
    main()
