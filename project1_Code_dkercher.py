import RPi.GPIO as GPIO
from gpiozero import LED, PWMLED, AngularServo
from time import sleep

###VARIABLES

#Rows of keypad (only using first two rows)
R1 = 5
R2 = 6
#R3 = 13
#R4 = 19

#Columns of keypad
C1 = 12
C2 = 16
C3 = 20
C4 = 21

#LEDs
#green
L1 = LED(22)
#yellow
L2 = PWMLED(17, frequency=100)
#red
L3 = LED(4)

#Servos
S1 = AngularServo(25, min_angle=-90, max_angle=90)

#Control variables
speed = 1
brightness = 1
increasing = False
dimming = False
button1Behavior = "A"
input = " "

###SETUPS

#GPIO setups
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(R1, GPIO.OUT)
GPIO.setup(R2, GPIO.OUT)
#GPIO.setup(R3, GPIO.OUT)
#GPIO.setup(R4, GPIO.OUT)

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

###Functions

#Read keypad columns and store button press as input
def readLine(line, characters):
	global input
	GPIO.output(line, GPIO.HIGH)
	if(GPIO.input(C1) == 1):
		input = characters[0]
	if(GPIO.input(C2) == 1):
		input = characters[1]
	if(GPIO.input(C3) == 1):
		input = characters[2]
	if(GPIO.input(C4) == 1):
		input = characters[3]
	GPIO.output(line, GPIO.LOW)

#Read keypad rows
def checkForInput():
	readLine(R1, ["1","2","3","A"])
	readLine(R2, ["4","5","6","B"])
	#Only using first two rows
	#readLine(R3, ["7","8","9","C"])
	#readLine(R4, ["*","0","#","D"])

#Interpret input to control functions
def interpretInput():
	global brightness, increasing, dimming, input, button1Behavior
	if (button1Behavior == "A" and input == "1" and increasing == False):
		print("\nStart increasing green LED blink speed")
		increasing = True
		input = " "
	elif (button1Behavior == "A" and input == "1" and increasing == True):
		print("\nStop increasing green LED blink speed")
		increasing = False
		input = " "
	elif (button1Behavior == "B" and input == "1" and dimming == False):
		print("\nStart dimming yellow LED brightness")
		dimming = True
		brightness = 0.1
		input = " "
	elif (button1Behavior == "B" and input == "1" and dimming == True):
		print("\nStop dimming yellow LED brightness")
		dimming = False
		brightness = 1
		input = " "
	elif (button1Behavior == "A" and input == "2"):
		print("\nButton 1: Now Controlling Yellow LED")
		button1Behavior = "B"
		input = " "
	elif (button1Behavior == "B" and input == "2"):
		print("\nButton 1: Now Controlling Green LED")
		button1Behavior = "A"
		input = " "
	elif (input == "4"):
		print("\nMoving Servo Clockwise & Turning On Red LED")
		S1.angle = -90
		L3.on()
		input = " "
	elif (input == "5"):
		print("\nMoving Servo to the Middle & Turning Off Red LED")
		S1.angle = 0
		L3.off()
		input = " "
	elif (input == "6"):
		print("\nMoving Servo Counterclockwise & Blinking Red LED 5 Times")
		S1.angle = 90
		L3.blink(1,1,5)
		input = " "

#Blink LEDs w/o PWM, check input in between waits to reduce input delay
def ledBlink(led,interval):
	led.on()
	sleep(interval)
	checkForInput()
	led.off()
	sleep(interval)
	checkForInput()

#Speed up blinking
def increaseSpeed():
      global speed
      speed -= 0.25
      if speed == 0:
              speed = 1

#Blink LEDs w/ PWM to control brightness, check input in between waits to reduce input delay
def ledPwmBlink(led, brightness, interval):
	led.value = brightness
	sleep(interval)
	checkForInput()
	led.value = 0
	sleep(interval)
	checkForInput()

#Run the program
try:
	#L1.off()
	#L2.off()
	#L3.off()
	S1.angle = 0

	print("""Button 1: Control LED (Currently Controlling Green LED)
		\nButton 2: Swap Button 1 Behavior
		\nButton 4: Move Servo Clockwise & Turn On Red LED
		\nButton 5: Move Servo to the Middle & Turn Off Red LED
		\nButton 6: Move Servo Counterclockwise & Blink Red LED 5 Times""")

	while True:
		ledBlink(L1, speed)
		ledPwmBlink(L2, brightness, 0.5)
		if increasing:
			increaseSpeed()
		checkForInput()
		interpretInput()
		sleep(0.2)

except KeyboardInterrupt:
	print("\nApplication stopped!")

