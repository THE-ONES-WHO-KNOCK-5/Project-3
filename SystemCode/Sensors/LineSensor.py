import GenericSensor
import grovepi


class LineSensor(GenericSensor):

    def __init__(self, portVal):
        self.portVal = portVal
        grovepi.pinMode(portVal, "INPUT")

    def getVal(self):
        return grovepi.digitalRead(self.portVal)
