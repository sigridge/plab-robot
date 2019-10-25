from PIL import Image
import ultrasonic
import reflectance_sensors
import camera


class Sensob:
    """Superclass for the Sensob classes"""

    def __init__(self):
        """Initializes the sensob objects with sensors and value"""
        self.sensors = None
        self.value = None

    def update(self):
        """Updates all the sensors in the sensob with the update function to the sensor"""
        self.sensors.update()

    def get_value(self):
        """returns the value"""
        return self.value

    def reset(self):
        """resets the sensors with their reset function"""
        self.sensors.reset()


class DistanceSensob(Sensob):
    """Distance Sensob class, used for calculating distances
    value: distance in cm"""

    def __init__(self):
        """Initializes the object with an Ultrasonic sensor and sets the value to the default
        sensor value"""
        super(DistanceSensob, self).__init__()
        self.sensors = ultrasonic.Ultrasonic()
        self.value = self.sensors.get_value()

    def update(self):
        """updates the sensor and updates the value"""
        self.value = self.sensors.update()

    def reset(self):
        """resets the sensor, and also resets the value"""
        self.sensors.reset()
        self.value = self.sensors.get_value()


class IRSensob(Sensob):
    """IR sensob class, used for checking reflected light under robot"""

    def __init__(self):
        """initializes the sensor, and sets the value to default value"""
        super(IRSensob, self).__init__()
        self.sensors = reflectance_sensors.ReflectanceSensors()
        self.value = self.sensors.get_value()

    def update(self):
        """Updates the sensor and sets the value to an 6 index array"""
        self.value = self.sensors.update()

    def reset(self):
        """Resets the sensors and value"""
        self.sensors.reset()
        self.value = self.sensors.get_value()

    def get_value(self):
        """Returns true if one of the array value is dark, else returns false"""
        return min(self.value)


class CameraSensob(Sensob):
    """Camera Sensob class, used for checking amount of green in a picture"""

    def __init__(self):
        """Initializes the class with the sensor and value"""
        super(CameraSensob, self).__init__()
        self.sensors = camera.Camera()
        self.value = self.sensors.get_value()

    def update(self):
        """Updates the sensor and sets the value"""
        self.value = self.sensors.update()
        print("******* Smile ^^")

    def reset(self):
        """Resets the sensor and the value"""
        self.sensors.reset()
        self.value = self.sensors.get_value()

    def get_value(self):
        pict = self.value
        img = list(pict.getdata())
        counter = 0
        for i in img:
            if (i[0] <= 150) and (i[1] >= 150) and (i[2] <= 150):
                counter += 1
        return counter/len(img)

