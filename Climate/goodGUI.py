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
#import serial

class UI(QMainWindow):
	def __init__(self):
		super(UI, self).__init__()
		uic.loadUi("coolUI.ui", self)
		self.show()
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.loop)
		self.timer.start(100)

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

		self.angleTest.clicked.connect(self.angle)

	def paintEvent(self, event):
		painter = QtGui.QPainter(self)
		painter.setPen(QtCore.Qt.white)
		#pic = QPixmap("profile.png")
		painter.translate(600, 10)
		painter.rotate(-10)
		#painter.drawPixmap(0, 0, pic)
		painter.drawText(0,0, "hello")
		painter.end()


	def loop(self):
		print("running")

	def setBoth(self):
		self.clearAll()
		self.both_L.setStyleSheet("background-color: rgb(61, 174, 233);")

	def setFeet(self):
		self.clearAll()
		self.feet_L.setStyleSheet("background-color: rgb(61, 174, 233);")

	def setHead(self):
		self.clearAll()
		self.head_L.setStyleSheet("background-color: rgb(61, 174, 233);")

	def setFeetDef(self):
		self.clearAll()
		self.feetDef_L.setStyleSheet("background-color: rgb(61, 174, 233);")

	def setDefrost(self):
		self.clearAll()
		self.defrost_L.setStyleSheet("background-color: rgb(61, 174, 233);")

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
			return
		if self.cooling == 1:
			self.AC_L.setStyleSheet("background-color: rgb(52, 59, 72);")
			self.cooling = 0
			return

	def setInsideAir(self):
		self.outsideAir_L.setStyleSheet("background-color: rgb(52, 59, 72);")
		self.insideAir_L.setStyleSheet("background-color: rgb(61, 174, 233);")
		
	def setOutsideAir(self):
		self.insideAir_L.setStyleSheet("background-color: rgb(52, 59, 72);")
		self.outsideAir_L.setStyleSheet("background-color: rgb(61, 174, 233);")

	def setDayLight(self):
		if self.bright == 0:
			self.dayLight_L.setStyleSheet("background-color: rgb(255, 255, 255);")
			self.bright = 1
			return
		if self.bright == 1:
			self.dayLight_L.setStyleSheet("background-color: rgb(52, 59, 72);")
			self.bright = 0
			return

	def angle(self):
		for i in range(-30, 30):
			time.sleep(0.5)

	def clearAll(self):
		self.both_L.setStyleSheet("background-color: rgb(52, 59, 72);")
		self.feet_L.setStyleSheet("background-color: rgb(52, 59, 72);")
		self.head_L.setStyleSheet("background-color: rgb(52, 59, 72);")
		self.feetDef_L.setStyleSheet("background-color: rgb(52, 59, 72);")
		self.defrost_L.setStyleSheet("background-color: rgb(52, 59, 72);")


app = QApplication(sys.argv)        # start PyQT
window = UI()
#window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
window.show()
app.exec_()