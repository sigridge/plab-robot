"""The main behaviour class and different versions as
subclasses that implements the methods differently"""


class Behavior:
    """The main behavior class, describes the different methods, and implements dummy methods"""

    def __init__(self, bbcon):
        """Initializes the different variables"""
        self.bbcon = bbcon
        self.sensobs = None  # a single sensob, or an array of them
        self.motor_recs = None  # Specific to the behaviour
        self.active_flag = False  # True if active, false if inactive
        self.halt_request = None  # True if the behaviour wants the robot to shut down
        self.priority = 1  # How important this specific behaviour is in relation to the others
        # a float in the range [0,1] that indicates how important the behaviour
        # is based on the current conditions
        self.match_degree = 0.0
        self.weight = self.priority * self.match_degree

    def consider_activation(self):
        """Called when the behaviour is active. Checks if it should deactivate and does so if needed"""

    def consider_activation(self):
        """Called when the behaviour is inactive. Checks if it should activate and does so if needed"""

    def update(self):
        """The main interface between bbcon and behaviour.
        Updates the activity status, calls sense_and_act, updates weight"""

    def sense_and_act(self):
        """Computations that uses sensob readings to produce motor recommendations"""
