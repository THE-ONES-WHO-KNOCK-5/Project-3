from SystemCode.System.Subsystems.TwoWheelDriveTrain import TwoWheelDriveTrain
import brickpi3

class Robot(object):
    BP = brickpi3.BrickPi3()
    drivetrain = None

    def __int__(self):
        self.drivetrain = TwoWheelDriveTrain(self.BP.PORT_B,self.BP.PORT_C)

    def periodic(self):
        self.drivetrain.periodic()