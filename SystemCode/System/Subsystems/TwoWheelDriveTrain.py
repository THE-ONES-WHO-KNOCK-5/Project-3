import GenericSubsystem
from SystemCode.Motors.GenericMotor import GenericMotor
class TwoWheelDriveTrain(GenericSubsystem):
    motorL = None
    motorR = None
    def __int__(self, motorL: GenericMotor, motorR: GenericMotor):
        self.motorR = motorR
        self.motorL = motorL

    def setArcade(self, forward, turn):
        self.motorL.setSpeed(forward - turn)
        self.motorR.setSpeed(forward + turn)

    def setTank(self, leftPow, rightPow):
        self.motorL.setSpeed(leftPow)
        self.motorR.setSpeed(rightPow)

    def periodic(self):
        pass