from PyQt5 import QtCore, QtWidgets, QtGui, Qt, uic
import sys
import os
import glob
import time
from os import path
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QColor
from mpu6050 import mpu6050
import math
import gpiod
from subprocess import call
from adafruit_servokit import ServoKit
from numpy import interp

kit = ServoKit(channels=16)
#kit.servo[0].actuation_range = 500
chip = gpiod.Chip('gpiochip4')
fanLow = chip.get_line(17)
fanMed1 = chip.get_line(18)
fanMed2 = chip.get_line(15)
fanHigh = chip.get_line(14)
lights = chip.get_line(25)
driver = chip.get_line(8)
passenger = chip.get_line(7)
acRelay = chip.get_line(6)

killPin = chip.get_line(23)

fanLow.request(consumer="Relay", type=gpiod.LINE_REQ_DIR_OUT, flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_UP)
fanMed1.request(consumer="Relay", type=gpiod.LINE_REQ_DIR_OUT, flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_UP)
fanMed2.request(consumer="Relay", type=gpiod.LINE_REQ_DIR_OUT, flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_UP)
fanHigh.request(consumer="Relay", type=gpiod.LINE_REQ_DIR_OUT, flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_UP)
lights.request(consumer="Relay", type=gpiod.LINE_REQ_DIR_OUT, flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_UP)
driver.request(consumer="Relay", type=gpiod.LINE_REQ_DIR_OUT, flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_UP)
passenger.request(consumer="Relay", type=gpiod.LINE_REQ_DIR_OUT, flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_UP)
acRelay.request(consumer="Relay", type=gpiod.LINE_REQ_DIR_OUT, flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_UP)

killPin.request(consumer="Button", type=gpiod.LINE_REQ_DIR_IN, flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_UP)

fanLow.set_value(1)
fanMed1.set_value(1)
fanMed2.set_value(1)
fanHigh.set_value(1)
lights.set_value(1)
driver.set_value(1)
passenger.set_value(1)
acRelay.set_value(1)

sensor = mpu6050(0X68)
pitches = [0]*10
rolls = [0]*10
counter = 0

class UI(QMainWindow):
	def __init__(self):
		super(UI, self).__init__()
		uic.loadUi("/home/acar/repos/Stacy/climate2/coolUI.ui", self)
		self.show()
		self.showMaximized()
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.loop)
		self.timer.start(50)
		self.setCursor(Qt.BlankCursor)

		self.counter = 0
		self.seatHeating = 0
		self.seatHeating_2 = 0
		self.cooling = 0
		self.bright = 0
		self.pitch = 0
		self.roll = 0

		self.both.clicked.connect(self.setBoth)
		self.feet.clicked.connect(self.setFeet)
		self.head.clicked.connect(self.setHead)
		self.feetDef.clicked.connect(self.setFeetDef)
		self.defrost.clicked.connect(self.setDefrost)

		self.heatSeater.clicked.connect(self.setHeatSeater)
		self.heatSeater_2.clicked.connect(self.setHeatSeater_2)

		self.AC.clicked.connect(self.setAC)

		self.insideAir.clicked.connect(self.setInsideAir)
		self.outsideAir.clicked.connect(self.setOutsideAir)

		self.dayLight.clicked.connect(self.setDayLight)

		self.tempSlider.valueChanged.connect(self.setTemp)
		self.fanSlider.valueChanged.connect(self.setFan)
		self.sensor = mpu6050(0X68)
		self.pitches = [0]*10
		self.rolls = [0]*10
		self.counter1 = 0
		self.lastPitch = 0
		self.lastRoll = 0
		self.setBoth()

	def loop(self):
		x = float(self.sensor.get_accel_data()['x'])
		y = float(self.sensor.get_accel_data()['y'])
		z = float(self.sensor.get_accel_data()['z'])

		pitch = math.degrees(math.atan(y/z))
		roll = math.degrees(math.atan(x/z))
		self.pitches.append(pitch)
		self.rolls.append(roll)
		self.pitches.pop(0)
		self.rolls.pop(0)

		if self.counter1 == 9:
			avgPitch = sum(self.pitches)/len(self.pitches)
			avgRoll = sum(self.rolls)/len(self.rolls)
			self.angle(avgPitch, avgRoll)
			self.counter1 = 0
		self.counter1 += 1

		if killPin.get_value() == 1:
			call("sudo shutdown -h now", shell=True)

	def setBoth(self):
		self.clearAll()
		self.both_L.setStyleSheet("background-color: rgb(61, 174, 233);")
		kit.servo[1].angle = 45 #45-130 deg, [1] = top servo (def)
		kit.servo[2].angle = 88 #45-130 deg, [2] = bottom servo
		print("both_")

	def setFeet(self):
		self.clearAll()
		self.feet_L.setStyleSheet("background-color: rgb(61, 174, 233);")
		kit.servo[2].angle = 130 #45-130 deg, [2] = bottom servo
		print("feet_")

	def setHead(self):
		self.clearAll()
		self.head_L.setStyleSheet("background-color: rgb(61, 174, 233);")
		kit.servo[1].angle = 45 #45-130 deg
		kit.servo[2].angle = 45 #45-130 deg
		print("head_")

	def setFeetDef(self):
		self.clearAll()
		self.feetDef_L.setStyleSheet("background-color: rgb(61, 174, 233);")
		kit.servo[1].angle = 130 #45-130 deg
		kit.servo[2].angle = 88 #45-130 deg
		print("def_f")

	def setDefrost(self):
		self.clearAll()
		self.defrost_L.setStyleSheet("background-color: rgb(61, 174, 233);")
		kit.servo[1].angle = 130 #45-130 deg
		kit.servo[2].angle = 45 #45-130 deg
		print("deff_")

	def setHeatSeater(self):
		if self.seatHeating == 0:
			self.heatSeater_L.setStyleSheet("background-color: rgb(208, 0, 0);")
			self.seatHeating = 1
			driver.set_value(0)
			return
		if self.seatHeating == 1:
			self.heatSeater_L.setStyleSheet("background-color: rgb(52, 59, 72);")
			self.seatHeating = 0
			driver.set_value(1)
			return

	def setHeatSeater_2(self):
		if self.seatHeating_2 == 0:
			self.heatSeater_L_2.setStyleSheet("background-color: rgb(208, 0, 0);")
			self.seatHeating_2 = 1
			passenger.set_value(0)
			return
		if self.seatHeating_2 == 1:
			self.heatSeater_L_2.setStyleSheet("background-color: rgb(52, 59, 72);")
			self.seatHeating_2 = 0
			passenger.set_value(1)
			return

	def setAC(self):
		if self.cooling == 0:
			self.AC_L.setStyleSheet("background-color: rgb(0, 208, 0);")
			self.cooling = 1
			acRelay.set_value(0)
			return
		if self.cooling == 1:
			self.AC_L.setStyleSheet("background-color: rgb(52, 59, 72);")
			self.cooling = 0
			acRelay.set_value(1)
			return

	def setInsideAir(self):
		self.outsideAir_L.setStyleSheet("background-color: rgb(52, 59, 72);")
		self.insideAir_L.setStyleSheet("background-color: rgb(61, 174, 233);")
		kit.servo[3].angle = 0 #0-90 deg, [3] = source servo

	def setOutsideAir(self):
		self.insideAir_L.setStyleSheet("background-color: rgb(52, 59, 72);")
		self.outsideAir_L.setStyleSheet("background-color: rgb(61, 174, 233);")
		kit.servo[3].angle = 90 #0-90 deg, [3] = source servo

	def setDayLight(self):
		if self.bright == 0:
			self.dayLight_L.setStyleSheet("background-color: rgb(255, 255, 255);")
			self.bright = 1
			lights.set_value(0)
			return
		if self.bright == 1:
			self.dayLight_L.setStyleSheet("background-color: rgb(52, 59, 72);")
			self.bright = 0
			lights.set_value(1)
			return

	def angle(self, pitch, roll):
		newPitch = pitch - self.lastPitch
		newRoll = roll - self.lastRoll
		self.pitchSlider.setValue(round(pitch))
		self.rollSlider.setValue(round(roll))
		self.lastPitch = pitch
		self.lastRoll = roll
		self.pitchLabel.setText(str(round(pitch)) + u'\xb0')
		self.rollLabel.setText(str(round(roll)) + u'\xb0')

	def setTemp(self):
		t = self.tempSlider.value()
		print(t)
		tempAngle = round(interp(t,[60,90],[0,66]))
		print(tempAngle)
		kit.servo[0].angle = tempAngle

	def setFan(self):
		if self.fanSlider.value() == 0:
			fanLow.set_value(1)
			fanMed1.set_value(1)
			fanMed2.set_value(1)
			fanHigh.set_value(1)
		if self.fanSlider.value() == 1:
			fanLow.set_value(0)
			fanMed1.set_value(1)
			fanMed2.set_value(1)
			fanHigh.set_value(1)
		if self.fanSlider.value() == 2:
			fanLow.set_value(0)
			fanMed1.set_value(0)
			fanMed2.set_value(1)
			fanHigh.set_value(1)
		if self.fanSlider.value() == 3:
			fanLow.set_value(0)
			fanMed1.set_value(1)
			fanMed2.set_value(0)
			fanHigh.set_value(1)
		if self.fanSlider.value() == 4:
			fanLow.set_value(0)
			fanMed1.set_value(1)
			fanMed2.set_value(1)
			fanHigh.set_value(0)

	def clearAll(self):
		self.both_L.setStyleSheet("background-color: rgb(52, 59, 72);")
		self.feet_L.setStyleSheet("background-color: rgb(52, 59, 72);")
		self.head_L.setStyleSheet("background-color: rgb(52, 59, 72);")
		self.feetDef_L.setStyleSheet("background-color: rgb(52, 59, 72);")
		self.defrost_L.setStyleSheet("background-color: rgb(52, 59, 72);")


app = QApplication(sys.argv)        # start PyQT
window = UI()
window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
window.show()
app.exec_()
