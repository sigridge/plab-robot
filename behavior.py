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

    def consider_deactivation(self):
        """Called when the behaviour is active.
        Checks if it should deactivate and does so if needed"""

    def consider_activation(self):
        """Called when the behaviour is inactive.
        Checks if it should activate and does so if needed"""

    def update(self):
        """The main interface between bbcon and behaviour.
        Updates the activity status, calls sense_and_act, updates weight"""
        if self.active_flag:
            self.consider_deactivation()
        else:
            self.consider_activation()

        self.sense_and_act()
        self.update_weight()

    def sense_and_act(self):
        """Computations that uses sensob readings to produce motor recommendations.
        Updates match_degree"""

    def update_weight(self):
        """Computes the weight"""
        self.weight = self.priority * self.match_degree


class AvoidLineBehaviour(Behavior):
    """Behaviour for staying inside the restricted area"""
    def __init__(self):
        super(AvoidLineBehaviour, self).__init__()
        self.sensobs  # Set this
        self.priority = 1  # Tweak
        self.update_weight()

    def consider_activation(self):
        """Activates if the sensob sees the line"""

    def consider_deactivation(self):
        """Deactivates if the sensob doesn't see the line"""

    def sense_and_act(self):
        """Sets motor recommendations to turn away from the line. Updates match_degree"""


class CollisionDetectionBehaviour(Behavior):
    """Detects an obstacle and halts the robot. OBS: Halt_request is always True"""
    def __init__(self):
        super(CollisionDetectionBehaviour, self).__init__()
        self.sensobs  # Set this
        self.halt_request = True
        self.priority = 1  # Tweak
        self.update_weight()

    def consider_deactivation(self):
        """deactivates if no obstacles"""

    def consider_activation(self):
        """Activates if obstacle"""

    def sense_and_act(self):
        """Updates match_degree based on proximity"""


class AvoidObstacleBehaviour(Behavior):
    """Activates if the robot got halted by CollisionDetectionBehaviour.
    Tries to avoid the obstacle"""
    def __init__(self):
        super(AvoidObstacleBehaviour, self).__init__()
        self.sensobs  # Set this
        self.priority = 1  # Tweak
        self.update_weight()

    def consider_deactivation(self):
        """Deactivates if robot no longer halted (will need a var in CTRL for this)"""

    def consider_activation(self):
        """Activates if robot was halted (will need a var in CTRL for this)"""

    def sense_and_act(self):
        """Turns away from obstacle. Updates match_degree based on proximity"""


class AttackBehaviour(Behavior):
    """Crashes into the obstacle if it's red"""
    def __init__(self):
        super(AttackBehaviour, self).__init__()
        self.sensobs  # set this
        self.priority = 5  # Tweak, Must be high
        self.update_weight()

    def consider_deactivation(self):
        """Deactivates if the robot is no longer halted"""

    def consider_activation(self):
        """Activates if robot was halted AND the sensobs report X amount of green(?)"""

    def sense_and_act(self):
        """Rams into the obstacle. Match_degree based on proximity"""