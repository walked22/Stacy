import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

t0 = time.time()

while(!GPIO.input(4)):
	t1 = time.time()
	try:
		print(1 / ((t1-t0)/60))
	except ZeroDivisionError:
		pass
	t0 = t1