import math

class Manipulator:

    BP = None
    gateMotor = None
    climbMotor = None
    gRatio = 40/8
    mult1 = 0

    gateAngle = 70.5
    wedgeAngle = 42.5

    def __init__(self, BP, gateMotor, multiplier1):
        self.BP = BP
        self.gateMotor = gateMotor
        self.mult1 = multiplier1

    # set angle of gate relative to the wedge
    def setGateAngle(self, angle):
        self.BP.set_motor_position(self.gateMotor, angle * self.gRatio * self.mult1)
        

    # stop motor PID
    def stopMotor(self):
        self.BP.set_motor_dps(self.gateMotor, 0)

    # reset motor encoder
    def resetEncoders(self):
        self.BP.offset_motor_encoder(self.gateMotor, self.BP.get_motor_encoder(self.gateMotor) + (self.gateAngle - self.wedgeAngle))
