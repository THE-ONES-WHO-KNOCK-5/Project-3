import GenericSensor
import brickpi3

class TouchSensor(GenericSensor):
    portVal = None
    BP = None
    def __init__(self, BP, portVal):
        self.portVal = portVal
        self.BP = BP
        BP.set_sensor_type(portVal, BP.SENSOR_TYPE.TOUCH)

    def getValue(self):
        try:
            return self.BP.get_sensor(self.portVal)
        except brickpi3.SensorError as error:
            print(error)
            return False
