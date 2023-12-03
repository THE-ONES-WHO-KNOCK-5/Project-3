import math

class Manipulator:

    BP = None
    gateMotor = None
    climbMotor = None
    gRatio = 40/8
    mult1 = 0
    mult2 = 0

    gateAngle = 70.5
    wedgeAngle = 42.5

    def __init__(self, BP, gateMotor, climbMotor, multiplier1, multiplier2):
        self.BP = BP
        self.gateMotor = gateMotor
        self.climbMotor = climbMotor
        self.mult1 = multiplier1
        self.mult2 = multiplier2

    # set angle of gate relative to the wedge
    def setGateAngle(self, angle):
        self.BP.set_motor_position(self.gateMotor, angle * self.gRatio * self.mult1)

    def setClimbAngle(self, angle):
        self.BP.set_motor_position(self.climbMotor, angle * self.mult2)

    def setClimbSlow(self):
        motorAngle = self.BP.get_motor_encoder(self.climbMotor)
        self.BP.set_motor_dps(self.climbMotor, -30)
        while(abs(motorAngle) < 0.5):
            motorAngle = self.BP.get_motor_encoder(self.climbMotor)
        self.BP.set_motor_dps(self.climbMotor, 0)
        

    # stop motor PID
    def stopMotor(self):
        self.BP.set_motor_dps(self.gateMotor, 0)

    # reset motor encoder
    def resetEncoders(self):
        self.BP.offset_motor_encoder(self.gateMotor, self.BP.get_motor_encoder(self.gateMotor) + (self.gateAngle - self.wedgeAngle))
        self.BP.offset_motor_encoder(self.climbMotor, self.BP.get_motor_encoder(self.climbMotor))