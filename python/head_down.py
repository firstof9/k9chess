from Adafruit_PWM_Servo_Driver import PWM # enabling servo driver 

pwm = PWM(0x40)			# initialise the PWM device using the default address
pwm.setPWMFreq(60)		# set frequency to 60 Hz

pwm.setPWM(0, 0, 430)	# head up