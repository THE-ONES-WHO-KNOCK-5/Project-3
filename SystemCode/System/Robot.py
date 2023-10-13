from SystemCode.System.Scheduler import Scheduler
from SystemCode.System.Subsystems.TwoWheelDriveTrain import TwoWheelDriveTrain
import brickpi3
import time

class Robot(object):
    scheduler = None
    lastTime = time.time()
    BP = brickpi3.BrickPi3()
    drivetrain = None

    def __int__(self):
        self.scheduler = Scheduler()
        self.drivetrain = TwoWheelDriveTrain(self.BP.PORT_B,self.BP.PORT_C)


    def periodic(self):
        self.scheduler.executeList()
        self.scheduler.isFinished()

        self.drivetrain.periodic()
        time.sleep(0.02)
