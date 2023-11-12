import time
import brickpi3
import grovepi
import math


BP = brickpi3.BrickPi3()


ultrasonic_sensor_port = 4 # assign ultrasonic sensor port to D4


BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.TOUCH)  # Configure port 1 sensor type


leftMotor = BP.PORT_B
rightMotor = BP.PORT_C


end = False


cruiseDist = 35
collDist = 20


wheelRad = 8.5 / 2
degreeToCM = 1 / 360 * wheelRad * 2 * math.pi
lastPosition = None
BP.offset_motor_encoder(leftMotor, BP.get_motor_encoder(leftMotor))
BP.offset_motor_encoder(rightMotor, BP.get_motor_encoder(rightMotor))






# Before touch sensor is pressed, your program will be stuck in this loop
print("Press touch sensor on port 1 to run motors")
value = 0
while not value:
   try:
       dist = grovepi.ultrasonicRead(ultrasonic_sensor_port)
       print("dist: " + str(dist))
       value = BP.get_sensor(BP.PORT_1)
   except brickpi3.SensorError:
       value = 0
print("Starting...")


# Main logic   
try:
   while not end:
       dist = grovepi.ultrasonicRead(ultrasonic_sensor_port)
       print("dist: " + str(dist))
       #endVel = (BP.get_motor_encoder(driveMotor) - BP.get_motor_encoder(driveMotor)) / .2


       if(dist > cruiseDist):
           BP.set_motor_dps(leftMotor, -5 / degreeToCM)
           BP.set_motor_dps(rightMotor, -5 / degreeToCM)
       elif(dist > collDist):
           BP.set_motor_dps(leftMotor, -2 / degreeToCM)
           BP.set_motor_dps(rightMotor, -2 / degreeToCM)
       else:
           BP.set_motor_dps(leftMotor, -5 / degreeToCM)
           BP.set_motor_dps(rightMotor, 0 / degreeToCM)
           time.sleep(3.5)
           BP.set_motor_dps(leftMotor, -10 / degreeToCM)
           BP.set_motor_dps(rightMotor, -10 / degreeToCM)
           time.sleep(2.5)
           BP.set_motor_dps(leftMotor, 0 / degreeToCM)
           BP.set_motor_dps(rightMotor, -5 / degreeToCM)
           time.sleep(3.5)
           BP.set_motor_dps(leftMotor, 0 / degreeToCM)
           BP.set_motor_dps(rightMotor, 0 / degreeToCM)
           end = True


       #lastPosition = BP.get_motor_encoder(driveMotor)


       time.sleep(.2) # hold each loop/iteration for .2 seconds


except IOError as error:
   print(error)
except TypeError as error:
   print(error)
except KeyboardInterrupt:
   print("You pressed ctrl+C...")


BP.offset_motor_encoder(leftMotor, BP.get_motor_encoder(leftMotor))
BP.offset_motor_encoder(rightMotor, BP.get_motor_encoder(rightMotor))
# use reset_all() to return all motors and sensors to resting states
BP.reset_all()
