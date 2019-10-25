"""Impoterer fra en gitt motors fil"""
from motors import Motors
#from zumo_button import ZumoButton
#from time import sleep

class Motob():
    """Use this method: update([direction, speed])"""

    def __init__(self):
        self.motors = Motors()
        self.value = []

    def update(self, new_recommendation):
        """Receive a new motor recommendation, load it into the value slot, and operationalize it"""
        self.value = new_recommendation
        self.operationalize()
        print("******* Updated motob")

    def operationalize(self):
        """Convert a motor recommendation"""
        if self.value[0] == "F":
            self.motors.set_value([1, 1], 0.8)
            self.motors.forward(self.value[1], 0.2)
            print("******Moved forward")
        elif self.value[0] == "B":
            self.motors.set_value([-1, -1], 0.8)
            self.motors.backward(self.value[1], 0.2)
            print("******Moved Back")
        elif self.value[0] == "L":
            self.motors.set_value([0, self.value[1]], 0.8)
            self.motors.left(self.value[1], 1)
            print("******Moved Left")
        elif self.value[0] == "R":
            self.motors.set_value([self.value[1], 0], 0.8)
            self.motors.right(self.value[1], 1)
            print("******Moved Right")
        elif self.value[0] == "S":
            self.motors.stop()
            print("******Stopped")

#motob = Motob()
#ZumoButton().wait_for_press()
#sleep(2)
#motob.update(["F", 0.5])
#motob.update(["S"])
#motob.update(["L", 0.5])
#motob.update(["F", 0.8])
#motob.update(["R", 0.5])
#motob.update(["S"])
#motob.update(["F", 0.8])
#motob.update(["S"])
