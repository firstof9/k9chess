#
# Python controller for servo based K9
# Now superseded by K9PythonController
#
import sys   # allows for command line to be interpreted
import json  # enables creation of JSON strings
import time	 # enables the failsafe
       
from threading import Timer
from ws4py.client.threadedclient import WebSocketClient # enabling web sockets
from Adafruit_PWM_Servo_Driver import PWM # enabling servo driver 

pwm = PWM(0x40)					# initialise the PWM device using the default address
pwm.setPWMFreq(60)				# set frequency to 60 Hz

motorspeed = 0.0				# speed of motor (0 full reverse, 100 full forward)
steering = 0.0					# direction of steering (0 full left, 100 full right)

# retrieves current robot status and place in JSON string 
def getStatusInfo() :
    result = []
    global motorspeed
    global steering
    result = json.dumps({"type":"status","motorspeed": motorspeed,"steering": steering}, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=(',', ': '), encoding="utf-8", default=None, sort_keys=False)
    return result
	
# setMotorSpeed will set the servo pulse speed required
def setMotorSpeed(reqmotorspeed,reqsteering) :
    global motorspeed
    global steering
    global pwm
    # print "Set speed at " + str(reqmotorspeed) + " and steering at " + str(reqsteering)
    servoMotorMin = 150				# min pulse length out of 4096
    servoMotorNeutral = 361			# neutral position of motors
    servoMotorMax = 600				# max pulse length out of 4096
    servoSteeringMin = 220			# min pulse length out of 4096
    servoSteeringNeutral = 375		# neutral position of steering
    servoSteeringMax = 510			# max pulse length out of 4096
    # Determine the degree of travel for each servo
    SteeringTravelLeft = servoSteeringNeutral - servoSteeringMin
    SteeringTravelRight = servoSteeringMax - servoSteeringNeutral
    MotorTravelForward = servoMotorMax - servoMotorNeutral
    MotorTravelBackward = servoMotorNeutral - servoMotorMin
    # Set to default zero in case logic doesn't work
    motorspeed = servoMotorNeutral
    steering = servoSteeringNeutral
    # Calculate servo pulse speed
    # print reqmotorspeed
    # print (reqmotorspeed > 0)
    # print (reqmotorspeed <= 100)
    reqsteering = reqsteering * -1
    if ((reqmotorspeed > 0) and (reqmotorspeed <= 100)) : 
        motorspeed = servoMotorNeutral + ((reqmotorspeed/100) * MotorTravelForward)
    if ((reqmotorspeed < 0) and (reqmotorspeed >= -100)) :
        motorspeed = servoMotorNeutral + ((reqmotorspeed/100) * MotorTravelBackward)
    if ((reqsteering > 0) and (reqsteering <= 100)) :
        steering = servoSteeringNeutral + ((reqsteering/100) * SteeringTravelRight)   
    if ((reqsteering < 0) and (reqsteering >= -100)) :
        steering = servoSteeringNeutral + ((reqsteering/100) * SteeringTravelLeft)
    pwm.setPWM(2, 0, int(motorspeed))      # set motor speed to desired speed
    pwm.setPWM(1, 0, int(steering))        # set steering to desired angle
    print "Motorspeed: " + str(int(motorspeed)) + " Steering: " + str(int(steering))
    return	
  
def stopMotors() :
    setMotorSpeed(0.0,0.0)
    print "Emergency stop motors called"
    return

# manages socket to local node-RED server
class MotorClient(WebSocketClient) :
    def opened(self) :
        print "Connection to node-RED open"
        return
    def closed(self, code, reason=None) :
        print "Connection to node-RED closed down", code, reason
        return
        # browser commands with type 'navigation' are routed by node-RED to the motors socket
        # the navigation 'alive' command is sent automatically by the browser and relayed via node-RED
    def received_message(self, message) :
        global motorspeed
        global steering
        global failsafe
        message = str(message)
        # print message
        driveinfo = []
        driveinfo = json.loads(message)
        command = driveinfo["command"]
        if command == "alive" :
            failsafe.cancel()
            failsafe = Timer(1, stopMotors)
            # print "Failsafe reset"
            failsafe.start()
        else :
            motorspeed = float(driveinfo["motorspeed"])
            steering = float(driveinfo["steering"])
            setMotorSpeed(motorspeed, steering)
        return

try:
    failsafe = Timer(600, stopMotors) # creation of initial failsafe with long timeout 
    # print "Fail safe set for 10 mins" 
    ws = MotorClient('ws://127.0.0.1:1880/admin/ws/motors')
    ws.connect()
    # print "WS Connected"
    ws.run_forever()
except KeyboardInterrupt:
    stopMotors()
    ws.close()
