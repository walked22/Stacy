from w1thermsensor import W1ThermSensor, Unit
import time
import csv

tempList = [None, None]

def getTemp():
	with open('temps.csv', 'w') as f:
		writer = csv.writer(f)
		for sensor in W1ThermSensor.get_available_sensors():
			if str(sensor.id) == "0309979409fe":
				
				tempList[0] = str(round(sensor.get_temperature(Unit.DEGREES_F)))
			if str(sensor.id) == "030897942ebd":
				tempList[1] = str(round(sensor.get_temperature(Unit.DEGREES_F)))
		writer.writerow(tempList)
		
while True:
	try:
		getTemp()
	except:
		pass
	time.sleep(10)
