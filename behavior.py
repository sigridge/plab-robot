"""The main behaviour class and different versions as
subclasses that implements the methods differently"""
import sensob
DISTANCE_SENSOB = sensob.DistanceSensob()
IR_SENSOB = sensob.IRSensob()
CAMERA_SENSOB = sensob.CameraSensob()


class Behavior:
    """The main behavior class, describes the different methods, and implements dummy methods"""

    def __init__(self, bbcon):
        """Initializes the different variables"""
        self.bbcon = bbcon
        self.sensobs = None  # a single sensob, or an array of them
        self.motor_recs = None  # Specific to the behaviour
        self.active_flag = False  # True if active, false if inactive
        self.halt_request = False  # True if the behaviour wants the robot to shut down
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

    def get_weight(self):
        """Return the weight"""
        return self.weight

    def get_motor_recs(self):
        """Returns the motor_recs"""
        return self.motor_recs

    def get_sensob(self):
        """Returns sensob"""
        return self.sensobs

    def get_halt_request(self):
        """Returns """


class SearchBehaviour(Behavior):
    """Goes forward. Is always active"""
    def __init__(self, bbcon):
        super(SearchBehaviour, self).__init__(bbcon)
        self.active_flag = True
        self.motor_recs = ["F", 0.4]
        self.bbcon.activate_behavior(self)


    def update(self):
        """Does nothing"""



class AvoidLineBehaviour(Behavior):
    """Behaviour for staying inside the restricted area"""
    def __init__(self, bbcon):
        super(AvoidLineBehaviour, self).__init__(bbcon)
        self.sensobs = IR_SENSOB
        self.priority = 2  # Tweak
        self.update_weight()
        self.motor_recs = ["L", 0.5]
        self.bbcon.deactivate_behavior(self)

    def consider_activation(self):
        """Activates if the sensob sees the line"""
        if self.sensobs.get_value() >= 0.75:
            self.bbcon.activate_behavior(self)

    def consider_deactivation(self):
        """Deactivates if the sensob doesn't see the line"""
        if self.sensobs.get_value() < 0.75:
            self.bbcon.deactivate_behavior(self)

    def sense_and_act(self):
        """Sets motor recommendations to turn away from the line. Updates match_degree"""
        self.match_degree = self.sensobs.get_value()
        print("*******IR: ", self.sensobs.get_value())


class CollisionDetectionBehaviour(Behavior):
    """Detects an obstacle and halts the robot. OBS: Halt_request is always True"""
    def __init__(self, bbcon):
        super(CollisionDetectionBehaviour, self).__init__(bbcon)
        self.sensobs = DISTANCE_SENSOB
        self.halt_request = True
        self.priority = 3  # Tweak
        self.update_weight()
        self.motor_recs = ["S"]
        self.bbcon.deactivate_behavior(self)

    def consider_deactivation(self):
        """deactivates if no obstacles"""
        if self.sensobs.get_value() > 10:
            self.bbcon.deactivate_behavior(self)

    def consider_activation(self):
        """Activates if obstacle"""
        if self.sensobs.get_value() <= 10:
            self.bbcon.activate_behavior(self)

    def sense_and_act(self):
        """Updates match_degree based on proximity"""
        self.match_degree = self.sensobs.get_value() / 50


class AvoidObstacleBehaviour(Behavior):
    """Activates if the robot got halted by CollisionDetectionBehaviour.
    Tries to avoid the obstacle"""
    def __init__(self, bbcon):
        super(AvoidObstacleBehaviour, self).__init__(bbcon)
        self.sensobs = DISTANCE_SENSOB
        self.priority = 4  # Tweak
        self.update_weight()
        self.motor_recs = ["R", 0.5]
        self.bbcon.deactivate_behavior(self)

    def consider_deactivation(self):
        """Deactivates if robot no longer halted (will need a var in CTRL for this)"""
        if len(self.bbcon.motor_recs) != 1:
            self.bbcon.deactivate_behavior(self)

    def consider_activation(self):
        """Activates if robot was halted (will need a var in CTRL for this)"""
        if len(self.bbcon.motor_recs) == 1:
            self.bbcon.activate_behavior(self)

    def sense_and_act(self):
        """Turns away from obstacle. Updates match_degree based on proximity"""
        self.match_degree = self.sensobs.get_value() / 50


class AttackBehaviour(Behavior):
    """Crashes into the obstacle if it's red"""
    def __init__(self, bbcon):
        super(AttackBehaviour, self).__init__(bbcon)
        self.sensobs = CAMERA_SENSOB
        self.priority = 5  # Tweak, Must be high
        self.update_weight()
        self.motor_recs = ["F", 0.8]
        self.bbcon.deactivate_behavior(self)

    def update(self):
        """The main interface between bbcon and behaviour.
        Updates the activity status, calls sense_and_act, updates weight. Does not call sense_and_act if inactive"""
        if self.active_flag:
            self.consider_deactivation()
        else:
            self.consider_activation()

        if self.active_flag:
            self.sense_and_act()
            self.update_weight()

    def consider_deactivation(self):
        """Deactivates if the robot is no longer halted"""
        if len(self.bbcon.motor_recs) != 1:
            self.bbcon.deactivate_behavior(self)

    def consider_activation(self):
        """Activates if robot was halted AND the sensobs report X amount of green"""
        if len(self.bbcon.motor_recs) == 1 and self.sensobs.get_value() >= 0.6:
            self.bbcon.activate_behavior(self)

    def sense_and_act(self):
        """Rams into the obstacle. Match_degree based on amount of Green"""
        self.match_degree = self.sensobs.get_value()
