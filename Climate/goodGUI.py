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
import serial
from mpu6050 import mpu6050
import math

#s.system('modprobe w1-gpio')  # Turns on the GPIO module
#os.system('modprobe w1-therm') # Turns on the Temperature module

#base_dir = '/sys/bus/w1/devices/'
#device_folder = glob.glob(base_dir + '28-031097944331')[0]
#device_folder2 = glob.glob(base_dir + '28-0309979409fe')[0]
#device_file = device_folder + '/w1_slave'
#device_file2 = device_folder2 + '/w1_slave'

try:
	ser=serial.Serial("/dev/ttyACM0",9600)  #change ACM number as found from ls /dev/tty/ACM*
except:
	ser=serial.Serial("/dev/ttyACM1",9600)
	pass
ser.baudrate=9600

sensor = mpu6050(0X68)
pitches = [0]*10
rolls = [0]*10
counter = 0

class UI(QMainWindow):
	def __init__(self):
		super(UI, self).__init__()
		uic.loadUi("coolUI.ui", self)
		self.show()
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.loop)
		self.timer.start(10)

		self.counter = 0
		self.seatHeating = 0
		self.seatHeating_2 = 0
		self.cooling = 0
		self.bright = 0
		self.pitch = 0
		self.roll = 0

		profilePic = QtGui.QPixmap("profile.png").scaled(50, 50)
		scene = QGraphicsScene()
		scene.addPixmap(profilePic)
		self.profileView.setScene(scene)

		facePic = QtGui.QPixmap("face.png").scaled(50, 50)
		scene = QGraphicsScene()
		scene.addPixmap(facePic)
		self.faceView.setScene(scene)

		self.profileView.rotate(0)
		self.faceView.rotate(0)

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
			print("pitch: " + str(avgPitch))
			#print("roll: " + str(avgRoll))
			self.counter1 = 0
		self.counter1 += 1


	def setBoth(self):
		self.clearAll()
		self.both_L.setStyleSheet("background-color: rgb(61, 174, 233);")
		print("both_")
		ser.write(b'both_')

	def setFeet(self):
		self.clearAll()
		self.feet_L.setStyleSheet("background-color: rgb(61, 174, 233);")
		print("feet_")
		ser.write(b'feet_')

	def setHead(self):
		self.clearAll()
		self.head_L.setStyleSheet("background-color: rgb(61, 174, 233);")
		print("head_")
		ser.write(b'head_')

	def setFeetDef(self):
		self.clearAll()
		self.feetDef_L.setStyleSheet("background-color: rgb(61, 174, 233);")
		print("def_f")
		ser.write(b'def_f')

	def setDefrost(self):
		self.clearAll()
		self.defrost_L.setStyleSheet("background-color: rgb(61, 174, 233);")
		print("deff_")
		ser.write(b'deff_')

	def setHeatSeater(self):
		if self.seatHeating == 0:
			self.heatSeater_L.setStyleSheet("background-color: rgb(208, 0, 0);")
			self.seatHeating = 1
			return
		if self.seatHeating == 1:
			self.heatSeater_L.setStyleSheet("background-color: rgb(52, 59, 72);")
			self.seatHeating = 0
			return

	def setHeatSeater_2(self):
		if self.seatHeating_2 == 0:
			self.heatSeater_L_2.setStyleSheet("background-color: rgb(208, 0, 0);")
			self.seatHeating_2 = 1
			return
		if self.seatHeating_2 == 1:
			self.heatSeater_L_2.setStyleSheet("background-color: rgb(52, 59, 72);")
			self.seatHeating_2 = 0
			return

	def setAC(self):
		if self.cooling == 0:
			self.AC_L.setStyleSheet("background-color: rgb(0, 208, 0);")
			self.cooling = 1
			print("ac_on")
			ser.write(b'ac_on')
			return
		if self.cooling == 1:
			self.AC_L.setStyleSheet("background-color: rgb(52, 59, 72);")
			self.cooling = 0
			print("ac_ff")
			ser.write(b'ac_ff')
			return

	def setInsideAir(self):
		self.outsideAir_L.setStyleSheet("background-color: rgb(52, 59, 72);")
		self.insideAir_L.setStyleSheet("background-color: rgb(61, 174, 233);")
		print("circ_")
		ser.write(b'circ_')

	def setOutsideAir(self):
		self.insideAir_L.setStyleSheet("background-color: rgb(52, 59, 72);")
		self.outsideAir_L.setStyleSheet("background-color: rgb(61, 174, 233);")
		print("circn")
		ser.write(b'circn')

	def setDayLight(self):
		if self.bright == 0:
			self.dayLight_L.setStyleSheet("background-color: rgb(255, 255, 255);")
			self.bright = 1
			return
		if self.bright == 1:
			self.dayLight_L.setStyleSheet("background-color: rgb(52, 59, 72);")
			self.bright = 0
			return

	def angle(self, pitch, roll):
		newPitch = pitch - self.lastPitch
		newRoll = roll - self.lastRoll
		self.profileView.rotate(newPitch*-1)
		self.faceView.rotate(newRoll)
		self.lastPitch = pitch
		self.lastRoll = roll
		self.pitchLabel.setText(str(round(pitch)) + u'\xb0')
		self.rollLabel.setText(str(round(roll)) + u'\xb0')

	def setTemp(self):
		t = self.tempSlider.value()
		temp = str(t)+"deg"
		print(temp)
		ser.write(temp.encode())

	def setFan(self):
		fanSpeed = "fan_" + str(self.fanSlider.value())
		print(fanSpeed)
		ser.write(fanSpeed.encode())

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
