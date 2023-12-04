import time
import grovepi
import brickpi3
import math



from DriveTrain import DriveTrain
from Manipulator import Manipulator
from Gyroscope import Gyroscope
from Timer import Timer


# set up sys variables
startTime = time.time()
currTime = time.time()
run = False
status = "None"
# 10 6.5
MAXSPEED = 15
TURBOSPEED = 25
MINSPEED = 10
UPDATERATE = 0.05
NUMSTORED = 5
gatesNum = 0
BP = brickpi3.BrickPi3()

#set up drive motors
rightMotor = BP.PORT_B
leftMotor = BP.PORT_C
drive = DriveTrain(BP, leftMotor, rightMotor, 1, 1)
drive.resetEncoders()

# manipulator system
gateMotor = BP.PORT_D
manipulator = Manipulator(BP, gateMotor, -1)
GATEUP = 50
GATEDOWN = 170
manipulator.resetEncoders()

# set up line sensors
leftLine = 8
rightLine = 3

# set up touch sensor

# set up gyro
myGyro = Gyroscope(NUMSTORED, UPDATERATE)

# set up distance sensor
ultrasonic_sensor_port = 4 # assign ultrasonic sensor port to D4

def getDistance():
    dist = grovepi.ultrasonicRead(ultrasonic_sensor_port)
    return dist
    

# line following command
def lineFollow(maxSpeed, turnSpeed, turnRight):
    if(grovepi.digitalRead(rightLine) == 0 and grovepi.digitalRead(leftLine) == 0):
        drive.setCM(maxSpeed,maxSpeed)
        print("Full Speed")
    elif(grovepi.digitalRead(rightLine) == 0):
        drive.setCM(turnSpeed,-turnSpeed)
    elif(grovepi.digitalRead(leftLine) == 0):
        drive.setCM(-turnSpeed,turnSpeed)
    elif turnRight:
        drive.setCM(-turnSpeed,turnSpeed)
        time.sleep(0.5)
        drive.setCM(maxSpeed,maxSpeed)
        time.sleep(1.1)
        drive.setCM(turnSpeed, -turnSpeed)
        while(grovepi.digitalRead(rightLine) == 0):
            print("Finding Line")
    else:
        drive.setCM(maxSpeed,maxSpeed)

def leftEdgeFollow(maxSpeed, turnSpeed):
    if(grovepi.digitalRead(leftLine) == 1):
        drive.setCM(maxSpeed,turnSpeed)
        print("Turn Right")
    else:
        drive.setCM(turnSpeed,maxSpeed)

# drive a certain distance at a speed command
def driveDistance(disCM, speed):
    startDist = drive.getLeftCM()
    currDist = drive.getLeftCM()
    drive.setCM(speed,speed)
    while currDist - startDist <= disCM:
        currDist = drive.getLeftCM()
        myGyro.updateGyro()
        time.sleep(UPDATERATE)
    drive.setCM(0,0)

def turnAngle(angle):
    currAngle = 0
    diff = angle - currAngle
    mult = math.copysign(1, diff)
    while(abs(angle) > abs(currAngle)):
        currAngle = currAngle - (myGyro.getGyroValue()["z"] * UPDATERATE)
        drive.setCM(MINSPEED / 4 * mult, -MINSPEED / 4 * mult)
        myGyro.updateGyro()
        print("running", currAngle)
    print("done")
    drive.setCM(0, 0)

# 0.5 second and 1 mult will turn 45 degrees
def turnTime(sec, mult):
    drive.setCM(MINSPEED * mult, -MINSPEED * mult)
    time.sleep(sec)
    drive.setCM(0, 0)

def findLine():
    turnTime(1,-1)
    timer = Timer(7)
    drive.setCM(MINSPEED/4, -MINSPEED/4)
    while(grovepi.digitalRead(rightLine) == 1 and (not timer.isTime())):
        time.sleep(UPDATERATE)

    drive.setCM(0, 0)

# drop cargo command
def dropCargo():
    driveDistance(10, 5)
    manipulator.setGateAngle(GATEDOWN)
    print("Dropping cargo")
    time.sleep(2)
    manipulator.setGateAngle(GATEUP)
    print("closing cargo")

def climbHill():
    drive.setCM(-MINSPEED, -MINSPEED)
    time.sleep(0.75)
    drive.setCM(TURBOSPEED, TURBOSPEED)
    time.sleep(4)
    

# run program here
try:
    time.sleep(1)
    myGyro.updateGyro()
    manipulator.setGateAngle(GATEUP)

    site = int(input("Enter Site Location: "))
    state = {"state": "start", "site": site}
    gatesNum = 0

    findLine()
    time.sleep(100)
    
    while True:
        if getDistance() < 7:
            drive.setCM(0,0)
        # TODO add support for gyro and climb
        elif(myGyro.getGyroValue()["x"] > 15):
            climbHill()
        else:
            # counting how many gates entered
            if myGyro.isEnterGate():
                gatesNum = gatesNum + 1

            # if at correct site, turn right at next turn
            if gatesNum >= 5000:
                leftEdgeFollow(MAXSPEED,MINSPEED * 0.75)
            elif (gatesNum == 2 and state["state"] == 3) or gatesNum == state["site"]:
                # if at drop of location, then drop cargo, and then move out
                if (gatesNum == 3 and state["state"] == 3) or gatesNum == state["site"] + 1:
                    dropCargo()
                    gatesNum += 5000
                lineFollow(MAXSPEED,MINSPEED, True)
                print("whatttt")
            else:
                #leftEdgeFollow(MAXSPEED,MINSPEED * 0.75)
                lineFollow(MAXSPEED,MINSPEED, False)



        myGyro.updateGyro()
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