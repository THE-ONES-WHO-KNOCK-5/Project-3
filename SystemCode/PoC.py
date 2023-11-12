import brickpi3
import time
import grovepi


try:
    lastTime = time.time()
    BP = brickpi3.BrickPi3()
    touchSensor = BP.PORT_1
    BP.set_sensor_type(touchSensor, BP.SENSOR_TYPE.TOUCH)
    rightLine = 3
    leftLine = 4
    rightMotor = BP.PORT_B
    leftMotor = BP.PORT_C
    grovepi.pinMode(rightLine,"INPUT")
    grovepi.pinMode(leftLine,"INPUT")

    lastVal = False
    triggered = False
    lock = False
    
    while True:
        value = False
        
        try:
            value = BP.get_sensor(touchSensor)
            print("Right: " + str(grovepi.digitalRead(rightLine)) + " Left:" + str(grovepi.digitalRead(leftLine)) )

            if(value == True and lastVal == False):
                lock = not lock
            print(lock)
            if lock == True:
                turn = 0
                if(grovepi.digitalRead(rightLine) == 1 and grovepi.digitalRead(leftLine) == 1):
                    turn = 0
                elif(grovepi.digitalRead(rightLine) == 1):
                    turn = -10 # clockwise
                elif(grovepi.digitalRead(leftLine) == 1):
                    turn = 10 # counter-clockwise
                    
                BP.set_motor_power(rightMotor, -90 + turn) # right motor
                BP.set_motor_power(leftMotor, -90 - turn) # left motor
            else:
                BP.set_motor_power(rightMotor, 0)
                BP.set_motor_power(leftMotor, 0)

            lastVal = value

        except brickpi3.SensorError as error:
            print(error)
            
            
        time.sleep(0.02)        
        
except KeyboardInterrupt:
    print(error)
    BP.reset_all()


    
        

        

