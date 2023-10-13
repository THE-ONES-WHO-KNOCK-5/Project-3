import math
from abc import ABC, abstractmethod
import brickpi3
class GenericMotor(ABC):
    BP = brickpi3.BrickPi3()
    motorPort = None
    def __int__(self, motorPort):
        self.motorPort = motorPort
        self.BP.offset_motor_encoder(motorPort, self.BP.get_motor_encoder(motorPort))


    def getEncoderValue(self):
        return self.BP.get_motor_encoder(self.motorPort)

    def getDegrees(self):
        return self.getEncoderValue() * 0.5

    def getRadians(self):
        return self.getDegrees() * math.pi / 180

    def setDPS(self, DPS):
        self.BP.set_motor_dps(self.motorPort, DPS)

    def setRPM(self, RPM):
        self.BP.set_motor_dps(self.motorPort, RPM * 360)

    @abstractmethod
    def setPower(self, power):
        pass
    
    def resetEncoder(self):
        self.BP.offset_motor_encoder(self.motorPort, self.BP.get_motor_encoder(self.motorPort))
