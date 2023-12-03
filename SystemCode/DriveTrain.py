import math
import brickpi3


class DriveTrain:
    wheelRad = 8.5 / 2
    gRatio = 3
    degreeToCM = 1 / 360 * wheelRad * 2 * math.pi

    BP = None
    mPortL = None
    mPortR = None
    leftMult = None
    rightMult = None

    def __init__(self, BP, mPortL, mPortR, leftMult, rightMult):
        self.BP = BP
        self.mPortL = mPortL
        self.mPortR = mPortR
        self.leftMult = leftMult
        self.rightMult = rightMult

    def setCM(self, CMLeft, CMRight):
        self.BP.set_motor_dps(self.mPortL, self.leftMult * CMLeft / self.degreeToCM * self.gRatio)
        self.BP.set_motor_dps(self.mPortR, self.rightMult * CMRight / self.degreeToCM * self.gRatio)

    def resetEncoders(self):
        self.BP.offset_motor_encoder(self.mPortL, self.BP.get_motor_encoder(self.mPortL))
        self.BP.offset_motor_encoder(self.mPortR, self.BP.get_motor_encoder(self.mPortR))

    def getRightCM(self):
        return self.BP.get_motor_encoder(self.mPortR) * self.degreeToCM / self.gRatio
    
    def getLeftCM(self):
        return self.BP.get_motor_encoder(self.mPortL) * self.degreeToCM / self.gRatio
    
