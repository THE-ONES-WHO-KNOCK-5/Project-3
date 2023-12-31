import time
import grovepi
import brickpi3
import math



from DriveTrain import DriveTrain
from Manipulator import Manipulator
from Gyroscope import Gyroscope
from ColorSensor import ColorSensor



# set up sys variables
startTime = time.time()
currTime = time.time()
run = False
status = "None"
# 10 6.5
MAXSPEED = 15
MINSPEED = 6.5
UPDATERATE = 0.05
NUMSTORED = 5
BP = brickpi3.BrickPi3()

#set up drive motors
rightMotor = BP.PORT_B
leftMotor = BP.PORT_C
drive = DriveTrain(BP, leftMotor, rightMotor, 1, 1)
drive.resetEncoders()

# manipulator system
gateMotor = BP.PORT_D
manipulator = Manipulator(BP, gateMotor, -1)
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
myGyro = Gyroscope(NUMSTORED, UPDATERATE)

# set up Color Sensor
cSensor = ColorSensor(BP, BP.PORT_3)

# set up distance sensor
ultrasonic_sensor_port = 4 # assign ultrasonic sensor port to D4

    
def getDistance():
    dist = grovepi.ultrasonicRead(ultrasonic_sensor_port)
    return dist
    

# line following command
def lineFollow(maxSpeed, minSpeed, turnRight):
    if(grovepi.digitalRead(rightLine) == 0 and grovepi.digitalRead(leftLine) == 0):
        drive.setCM(maxSpeed,maxSpeed)
    elif(grovepi.digitalRead(rightLine) == 0):
        drive.setCM(maxSpeed,-minSpeed)
    elif(grovepi.digitalRead(leftLine) == 0):
        drive.setCM(-minSpeed,maxSpeed)
    elif turnRight:
        drive.setCM(maxSpeed,-minSpeed)

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
        myGyro.updateGyro()
        time.sleep(UPDATERATE)
    drive.setCM(0,0)

# drop cargo command
def dropCargo():
    drive.setCM(0,0)
    manipulator.setGateAngle(180)
    print("Dropping cargo")
    time.sleep(4)
    #driveDistance(8,5)
    manipulator.setGateAngle(0)
    print("closing cargo")
    manipulator.stopMotor()


# run program here
try:
    time.sleep(5)
    ##dropCargo()
    speed = float(input("speed: "))
    driveDistance(255/ 0.93, speed + (0.07 * 30))




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