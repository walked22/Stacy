from mpu6050 import mpu6050
import math
import time

sensor = mpu6050(0X68)
pitches = [0]*10
rolls = [0]*10
counter = 0

while(True):
	x = float(sensor.get_accel_data()['x'])
	y = float(sensor.get_accel_data()['y'])
	z = float(sensor.get_accel_data()['z'])

	pitch = math.degrees(math.atan(y/z))
	roll = math.degrees(math.atan(x/z))
	pitches.append(pitch)
	rolls.append(roll)
	pitches.pop(0)
	rolls.pop(0)

	if counter == 9:
		avgPitch = sum(pitches)/len(pitches)
		avgRoll = sum(rolls)/len(rolls)
		print("pitch: " + str(avgPitch))
		print("roll: " + str(avgRoll))
		counter = 0
	counter += 1
	time.sleep(0.1)
