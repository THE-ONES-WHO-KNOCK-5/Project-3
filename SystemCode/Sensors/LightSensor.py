import grovepi
import GenericSensor

class LightSensor(GenericSensor):

    def __int__(self, portVal):
        self.portVal = portVal
        grovepi.pinMode(portVal, "INPUT")

    def getVal(self):
        rawVal = groovepi.analogRead(self.portVal)
        return (float) (1023- rawVal) * 10 / rawVal