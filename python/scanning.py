import sys   # allows for command line to be interpreted
import time  # allows for delay
       
servoMin = 150			# min pulse length out of 4096
servoMax = 600			# max pulse length out of 4096
servo = 0				# default servo
value = 375				# default value for servo


from Adafruit_PWM_Servo_Driver import PWM # enabling servo driver 

pwm = PWM(0x40)			# initialise the PWM device using the default address
pwm.setPWMFreq(60)		# set frequency to 60 Hz

pwm.setPWM(3, 0, 400)	# ears in
time.sleep(0.75)
pwm.setPWM(3, 0, 600)	# ears out
time.sleep(0.75)

pwm.setPWM(3, 0, 400)	# ears in
time.sleep(0.75)
pwm.setPWM(3, 0, 600)	# ears out
time.sleep(0.75)

pwm.setPWM(3, 0, 400)	# ears in
time.sleep(0.75)
pwm.setPWM(3, 0, 600)	# ears out
time.sleep(0.75)