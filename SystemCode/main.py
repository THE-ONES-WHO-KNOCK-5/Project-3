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
TURBOSPEED = 30
MINSPEED = 10
UPDATERATE = 0.05
NUMSTORED = 5
gatesNum = 0
BP = brickpi3.BrickPi3()
climbCounter = 0
gateFlag = True

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

def edgeFollow(maxSpeed, turnSpeed, isWeight, isLeft):
    if isLeft:
        if(grovepi.digitalRead(leftLine) == 1):
            if isWeight:
                drive.setCM(20,-20/4)
            else:
                drive.setCM(maxSpeed,-turnSpeed)
        else:
            if isWeight:
                drive.setCM(-20/5,20)
            else:
                drive.setCM(turnSpeed,maxSpeed)
    else:
        if(grovepi.digitalRead(rightLine) == 1):
            if isWeight:
                drive.setCM(-20/4,20)
            else:
                drive.setCM(-turnSpeed,maxSpeed)
        else:
            if isWeight:
                drive.setCM(20,-20/5)
            else:
                drive.setCM(maxSpeed,turnSpeed)

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
    drive.setCM(0, 0)

# 0.5 second and 1 mult will turn 45 degrees
def turnTime(sec, mult):
    drive.setCM(MINSPEED * mult, -MINSPEED * mult)
    time.sleep(sec)
    drive.setCM(0, 0)

def findLine(turn):
    if turn:
        turnTime(1,-1)
        timer = Timer(7)
    else:
        timer = Timer(1)
    drive.setCM(MINSPEED, -MINSPEED)
    while(grovepi.digitalRead(rightLine) == 0):
        if(timer.isTime()):
            drive.setCM(MINSPEED/1.5, MINSPEED/1.5)
        time.sleep(UPDATERATE)
    drive.setCM(0, 0)

# drop cargo command
def dropCargo():
    driveDistance(35, 5)
    manipulator.setGateAngle(GATEDOWN)
    print("Dropping cargo")
    time.sleep(1.5)
    manipulator.setGateAngle(GATEUP)
    print("closing cargo")
    drive.setCM(0, 0)

def climbHill(ifHill):
    drive.setCM(-MINSPEED, -MINSPEED)
    time.sleep(0.75)
    drive.setCM(TURBOSPEED, TURBOSPEED)
    if ifHill:
        time.sleep(4.35)
    else:
        time.sleep(1.5)
    drive.setCM(0,0)
    

# run program here
try:
    time.sleep(1)
    myGyro.updateGyro()
    manipulator.setGateAngle(GATEUP)

    site = int(input("Enter Site Location: "))
    state = {"state": "start", "site": site}
    gatesNum = 0

    """
    while True:
        leftEdgeFollow(MAXSPEED,MINSPEED * 0.75, True)
        myGyro.updateGyro()
        time.sleep(UPDATERATE)
    """
    
    while True:
        doneClimb = climbCounter <= 1
        print("Gate",gatesNum)
        if getDistance() < 7:
            drive.setCM(0,0)
        # TODO add support for gyro and climb
        elif(myGyro.getGyroValue()["x"] > 10 and doneClimb):
            climbHill(climbCounter != 0)
            findLine(False)
            climbCounter += 1
        else:
            # counting how many gates entered
            if myGyro.isEnterGate():
                gatesNum = gatesNum + 1

            # if at correct site, turn right at next turn
            if gatesNum >= 5000:
                edgeFollow(MAXSPEED,MINSPEED * 0.75, False, True)
            elif (gatesNum == 2 and state["site"] == 3) or gatesNum == state["site"]:
                # if at drop of location, then drop cargo, and then move out
                if (gatesNum == 2 and state["site"] == 3):
                    gateFlag = False
                    turnTime(1,1)
                    drive.setCM(15,15)
                    
                if gateFlag:
                    gateFlag = False

                if gatesNum == 3:
                    dropCargo()
                    gatesNum += 5000

                
                if not gateFlag:
                    lineFollow(MAXSPEED,MINSPEED, False)
                else:
                    edgeFollow(MAXSPEED,MINSPEED * 0.75, True, False)
            elif gatesNum == state["site"] + 1:
                dropCargo()
                gatesNum += 5000
            elif not doneClimb:
                edgeFollow(MAXSPEED,MINSPEED * 0.75, True, True)
            else:
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