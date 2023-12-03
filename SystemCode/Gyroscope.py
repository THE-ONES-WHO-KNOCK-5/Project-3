from MPU9250 import MPU9250
import math

class Gyroscope():

    NUMSTORED = None
    UPDATERATE = None
    myIMU = None
    MAGTHRESHOLD = 1000
    lastGateState = False
    angleList = [0]
    magList = [0]
    accelList = [0]
    gateList = [True]

    def __init__(self, NUMSTORED, UPDATERATE):
        self.myIMU = MPU9250(0x68)
        self.NUMSTORED = NUMSTORED
        self.UPDATERATE = UPDATERATE
        



    def updateGyro(self):
        # updates magnetic sensor values
        listVal = self.myIMU.readMagnet()
        magMag = math.sqrt(listVal["x"]**2 + listVal["y"]**2 + listVal["z"]**2)
        if magMag != 0.0:
            self.magList.append(magMag) 
            if len(self.magList) > self.NUMSTORED:
                self.magList.pop(0)
        
        # update Gate Values
        gateVAl = self.getMagChange() > self.MAGTHRESHOLD
        self.gateList.append(gateVAl) 
        if len(self.gateList) > self.NUMSTORED:
            self.gateList.pop(0)
        
        # gyro sensor values
        gyroVal = self.myIMU.readGyro()
        self.angleList.append(gyroVal) 
        if len(self.angleList) > self.NUMSTORED:
            self.angleList.pop(0)

        # updates acceleration values
        accelVal = self.myIMU.readAccel()
        self.accelList.append(accelVal) 
        if len(self.accelList) > self.NUMSTORED:
            self.accelList.pop(0)

    def getMagValue(self):
        return sum(self.magList)/len(self.magList)

    def getMagChange(self):
        rateList = []
        for i in range(len(self.magList) - 1):
            rateList.append((self.magList[i+1] - self.magList[i]) / (self.UPDATERATE))

        return sum(rateList) / (len(rateList))

    def getGyroValue(self):
        return {"x": self.angleList[-1]["x"], "y": self.angleList[-1]["y"], "z": self.angleList[-1]["z"]}
    
    def isEnterGate(self):
        return self.gateList[-1] == True and self.gateList[-2] == False