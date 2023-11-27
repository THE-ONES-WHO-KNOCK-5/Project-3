import time
import grovepi
import brickpi3
import math
from MPU9250 import MPU9250


from DriveTrain import DriveTrain
from Manipulator import Manipulator


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
myIMU = MPU9250(0x68)
angleList = []
magList = []
accelList = []

# set up distance sensor
ultrasonic_sensor_port = 4 # assign ultrasonic sensor port to D4


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

# get button value
def getButton():
    try:
        return BP.get_sensor(touchSensor)
    except brickpi3.SensorError as error:
        print(error)
        return False
    
def getDistance():
    dist = grovepi.ultrasonicRead(ultrasonic_sensor_port)
    return dist

def updateGyro():
    # updates magnetic sensor values
    listVal = myIMU.readMagnet()
    magMag = math.sqrt(listVal["x"]**2 + listVal["y"]**2 + listVal["z"]**2)
    if magMag != 0.0:
        magList.append(magMag) 
        if len(magList) > NUMSTORED:
            magList.pop(0)
    
    # gyro sensor values
    gyroVal = myIMU.readGyro()
    angleList.append(gyroVal) 
    if len(gyroVal) > NUMSTORED:
        angleList.pop(0)

    # updates acceleration values
    accelVal = myIMU.readAccel()
    accelList.append(accelVal) 
    if len(accelVal) > NUMSTORED:
        accelList.pop(0)

def getMagValue():
    return sum(magList)/len(magList)

def getMagChange():
    return (magList[-1] - magList[0]) / (UPDATERATE * len(magList))

def getGyroValue():
    return {"x": angleList[-1]["x"], "y":angleList[-1]["y"], "z":angleList[-1]["z"]}
    

# line following command
def lineFollow(maxSpeed, minSpeed):
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
    time.sleep(1)
    ##dropCargo()
    updateGyro()
    
    while True:
        print(angleList)

        """
        if(diff <= 1000000000):
            lineFollow()
        else:
            dropCargo()
        """
        updateGyro()
        time.sleep(UPDATERATE)




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