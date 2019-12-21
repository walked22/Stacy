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
#import RPi.GPIO as GPIO

count = 0
num = 0

os.system('modprobe w1-gpio')  # Turns on the GPIO module
os.system('modprobe w1-therm') # Turns on the Temperature module

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28-031097944331')[0]
device_folder2 = glob.glob(base_dir + '28-0309979409fe')[0]
device_file = device_folder + '/w1_slave'
device_file2 = device_folder2 + '/w1_slave'

try:
	ser=serial.Serial("/dev/ttyACM0",9600)  #change ACM number as found from ls /dev/tty/ACM*
except:
	ser=serial.Serial("/dev/ttyACM1",9600)
	pass
ser.baudrate=9600

qtCreatorFile = "untitled.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class mainthread(QThread):
	TEMPSignal = pyqtSignal('PyQt_PyObject')
	TEMP2Signal = pyqtSignal('PyQt_PyObject')

	def __init__(self):                                            # PyQT initialization function
		QThread.__init__(self)

	def __del__(self):
		self.wait()

	def read_temp_raw(self):
		f = open(device_file, 'r') # Opens the temperature device file
		lines = f.readlines() # Returns the text
		f.close()
		return lines

	def read_temp_2(self):
		f2 = open(device_file2, 'r')
		lines2 = f2.readlines()
		f2.close()
		return lines2

	def run(self):
		while(True):
			lines = self.read_temp_raw() # Read the temperature 'device file'
			lines2 = self.read_temp_2()
			while lines[0].strip()[-3:] != 'YES':
				time.sleep(0.2)
				lines = self.read_temp_raw()
			equals_pos = lines[1].find('t=')
			if equals_pos != -1:
				temp_string = lines[1][equals_pos+2:]
				temp_c = float(temp_string) / 1000.0
				temp_f = temp_c * 9.0 / 5.0 + 32.0
				self.TEMPSignal.emit("%.1f" % temp_f)
			while lines2[0].strip()[-3:] != 'YES':
				time.sleep(0.2)
				lines2 = self.read_temp_2()
			equals_pos2 = lines2[1].find('t=')
			if equals_pos2 != -1:
				temp_string2 = lines2[1][equals_pos2+2:]
				temp_c2 = float(temp_string2) / 1000.0
				temp_f2 = temp_c2 * 9.0 / 5.0 + 32.0
				self.TEMP2Signal.emit("%.1f" % temp_f2)

class MainApp(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self, parent=None):
		super(MainApp, self).__init__(parent)
		QMainWindow.__init__(self)
		self.setupUi(self)
		self.mythread1 = mainthread()
		self.mythread1.start()
		self.mythread1.TEMPSignal.connect(self.tempDisp)
		self.mythread1.TEMPSignal.connect(self.starter)
		self.mythread1.TEMP2Signal.connect(self.temp2Disp)
		self.setStyle(QStyleFactory.create('breeze'))
		self.setStyleSheet("QMainWindow {background: rgb(35,35,35);}")
		self.insideTemp.setStyleSheet('color: white')
		self.up.clicked.connect(self.fan_up)
		self.down.clicked.connect(self.fan_down)
		self.ac.clicked.connect(self.air_conditioning)
		self.circ.clicked.connect(self.circulation)
		self.head.clicked.connect(self.head_air)
		self.feet.clicked.connect(self.feet_air)
		self.both.clicked.connect(self.both_air)
		self.def_feet.clicked.connect(self.def_feet_air)
		self.deff.clicked.connect(self.deff_air)
		self.temp.valueChanged.connect(self.temp_change)
		self.ac.setStyleSheet("background-color: rgb(255,255,255)")
		self.f0.setStyleSheet("background-color: rgb(255,255,255)")
		self.f1.setStyleSheet("background-color: rgb(255,255,255)")
		self.f2.setStyleSheet("background-color: rgb(255,255,255)")
		self.f3.setStyleSheet("background-color: rgb(255,255,255)")
		self.up.setStyleSheet("background-color: rgb(255,255,255)")
		self.down.setStyleSheet("background-color: rgb(255,255,255)")
		self.TR.setStyleSheet("color: white")
		self.T2.setStyleSheet("color: white")
		self.TRL.setStyleSheet("color: white")
		self.T2L.setStyleSheet("color: white")
		self.color = "background-color: rgb(61, 174, 233)"

	def starter(self, t1):
		global num
		if num == 0:
			if float(t1) >= 85:
				ser.write(b'60deg')
				time.sleep(1)
				count = 3
				self.fan_up()
			if float(t1) <= 55:
				global count
				ser.write(b'90deg')
				time.sleep(1)
				count = 3
				self.fan_up()
		num += 1

	def tempDisp(self, temp):
		self.TR.setText(str(temp))

	def temp2Disp(self, temp):
		self.T2.setText(str(temp))

	def fan_up(self):
		global count
		if count == 0:
			self.f0.setStyleSheet(self.color)
			ser.write(b'fan_1')
		elif count == 1:
			self.f1.setStyleSheet(self.color)
			ser.write(b'fan_2')
		elif count == 2:
			self.f2.setStyleSheet(self.color)
			ser.write(b'fan_3')
		elif count == 3:
			self.f3.setStyleSheet(self.color)
			ser.write(b'fan_4')
			count = 2
		count += 1

	def fan_down(self):
		global count
		if count == 0:
			self.f0.setStyleSheet("background-color: rgb(255,255,255)")
			ser.write(b'fan_0')
			count = 1
		elif count == 1:
			self.f1.setStyleSheet("background-color: rgb(255,255,255)")
			ser.write(b'fan_1')
		elif count == 2:
			self.f2.setStyleSheet("background-color: rgb(255,255,255)")
			ser.write(b'fan_2')
		elif count == 3:
			self.f3.setStyleSheet("background-color: rgb(255,255,255)")
			ser.write(b'fan_3')
		count -= 1

	def air_conditioning(self):
		if self.ac.isChecked():
			ser.write(b'ac_on')
			self.ac.setStyleSheet(self.color)
		if self.ac.isChecked() == False:
			ser.write(b'ac_ff')
			self.ac.setStyleSheet("background-color: rgb(255,255,255)")


	def circulation(self):
		if self.circ.isChecked():
			ser.write(b'circ_')
			self.circ.setStyleSheet(self.color)
		if self.circ.isChecked() == False:
			ser.write(b'circn')
			self.circ.setStyleSheet("background-color: rgb(255,255,255)")

	def head_air(self):
		ser.write(b'head_')

	def feet_air(self): 
		ser.write(b'feet_')

	def both_air(self): 
		ser.write(b'both_')

	def def_feet_air(self):
		ser.write(b'def_f')

	def deff_air(self):
		ser.write(b'deff_')

	def temp_change(self):
		t = self.temp.value()
		temp = str(t)+"deg"
		ser.write(temp.encode())

def main():
	app = QApplication(sys.argv)        # start PyQT
	window = MainApp()
	window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
	window.show()
	app.exec_()

if __name__ == '__main__':              # run PyQT
	main()
