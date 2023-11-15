import time
import grovepi
import brickpi3
import math


from DriveTrain import DriveTrain
from Manipulator import Manipulator


BP = brickpi3.BrickPi3()

#set up drive motors
rightMotor = BP.PORT_B
leftMotor = BP.PORT_C
drive = DriveTrain(BP, leftMotor, rightMotor, 1, 1)
drive.resetEncoders()

# manipulator system
threadMotor = BP.PORT_A
gateMotor = BP.PORT_D
manipulator = Manipulator(BP, threadMotor, gateMotor)
manipulator.resetEncoders()

# set up line sensors
leftLine = 8
rightLine = 3

# set up touch sensor
touchSensor = BP.PORT_1
BP.set_sensor_type(touchSensor, BP.SENSOR_TYPE.TOUCH)
buttonNum = 0
lastVal = False
val = False

# set up gyro


magSensor = BP.PORT_3
BP.set_sensor_type(magSensor, BP.SENSOR_TYPE.CUSTOM, [BP.SENSOR_CUSTOM.PIN1_ADC])

# set up sys variables
startTime = time.time()
currTime = time.time()
run = False
status = "None"
maxSpeed = 10
minSpeed = 6.5

# get button value
def getButton():
    try:
        return BP.get_sensor(touchSensor)
    except brickpi3.SensorError as error:
        print(error)
        return False
    

# line following command
def lineFollow():
    if(grovepi.digitalRead(rightLine) == 0 and grovepi.digitalRead(leftLine) == 0):
        drive.setCM(maxSpeed,maxSpeed)
    elif(grovepi.digitalRead(rightLine) == 0):
        drive.setCM(maxSpeed,-minSpeed)
    elif(grovepi.digitalRead(leftLine) == 0):
        drive.setCM(-minSpeed,maxSpeed)
    else:
        drive.setCM(minSpeed,minSpeed)

# drive a certain distance at a speed command
def driveDistance(disCM, speed):
    startDist = drive.getLeftCM()
    currDist = drive.getLeftCM()
    drive.setCM(speed,speed)
    while currDist - startDist <= disCM:
        currDist = drive.getLeftCM()
        print(currDist - startDist)
    drive.setCM(0,0)

# drop cargo command
def dropCargo():
    drive.setCM(0,0)
    driveDistance(15,5)
    manipulator.setThreadSpeed(-0.5)
    manipulator.setGatePosition(1.25)
    time.sleep(4)
    manipulator.setThreadSpeed(0)
    driveDistance(8,5)
    manipulator.setGatePosition(0)


# run program here
try:
    time.sleep(1)
    ##driveDistance(200,50)

    
    driveDistance(65,5)
    drive.setCM(10,-5)
    time.sleep(1)
    driveDistance(20,5)
    dropCargo()
    driveDistance(25,5)
    
    while True:

        """
        if(diff <= 1000000000):
            lineFollow()
        else:
            dropCargo()
        """
        lineFollow()


except IOError as error:
    print(error)
    drive.setCM(0,0)
    drive.resetEncoders()
    manipulator.resetEncoders()
    BP.reset_all()
except TypeError as error:
    print(error)
    drive.setCM(0,0)
    drive.resetEncoders()
    manipulator.resetEncoders()
    BP.reset_all()
except KeyboardInterrupt:
    print("You pressed ctrl+C...")
    drive.setCM(0,0)
    drive.resetEncoders()
    manipulator.resetEncoders()
    BP.reset_all()