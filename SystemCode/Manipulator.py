import math

class Manipulator:

    BP = None
    threadMotor = None
    gateMotor = None

    def __init__(self, BP, threadMotor, gateMotor):
        self.BP = BP
        self.threadMotor = threadMotor
        self.gateMotor = gateMotor

    def setThreadSpeed(self, speedRot):
        self.BP.set_motor_dps(self.threadMotor, speedRot *360)

    def setgateSpeed(self, speedRot):
        self.BP.set_motor_dps(self.gateMotor, speedRot * 360)

    def setGatePosition(self, positionRot):
        self.BP.set_motor_position(self.gateMotor, positionRot * 360)

    def resetEncoders(self):
        self.BP.offset_motor_encoder(self.threadMotor, self.BP.get_motor_encoder(self.threadMotor))
        self.BP.offset_motor_encoder(self.gateMotor, self.BP.get_motor_encoder(self.gateMotor))