import ultrasonic
import reflectance_sensors
import camera
from PIL import Image


class Sensob:

    def __init__(self):
        self.sensors = None
        self.value = None

    def update(self):
        for sensor in self.sensors:
            sensor.update()

    def get_value(self):
        return self.value

    def reset(self):
        for sensor in self.sensors:
            sensor.update()


class DistanceSensob(Sensob):

    def __init__(self):
        self.sensors = ultrasonic.Ultrasonic()
        self.value = self.sensors.get_value()

    def update(self):
        self.value = self.sensors.update()

    def reset(self):
        self.sensors.reset()
        self.value = self.sensors.get_value()


class IRSensob(Sensob):

    def __init__(self):
        self.sensors = reflectance_sensors.ReflectanceSensors()
        self.value = self.sensors.get_value()

    def update(self):
        self.value = self.sensors.update()

    def reset(self):
        self.sensors.reset()
        self.value = self.sensors.get_value()

    def get_value(self):
        for i in range(length(self.value)):
            if self.value[i] < 200:
                return True
        return False


class CameraSensob(Sensob):

    def __init__(self):
        self.sensors = camera.Camera()
        self.value = self.sensors.get_value()

    def update(self):
        self.value = self.sensors.update()

    def reset(self):
        self.sensors.reset()

