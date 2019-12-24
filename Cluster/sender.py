from PyQt5 import QtCore, QtWidgets, QtGui, Qt, uic
import sys
import time
from os import path
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QColor
import serial
import math
import threading

qtCreatorFile = "sim.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MainApp(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self, parent=None):
		super(MainApp, self).__init__(parent)
		QMainWindow.__init__(self)
		self.setupUi(self)
		self.setStyle(QStyleFactory.create('breeze'))
		self.setStyleSheet("QMainWindow {background: rgb(35,35,35);}")
		x = threading.Thread(target=self.thread1)
		x.start()

	def thread1(self):
		while True:
			speed = self.speed.value()
			rpm = self.RPM.value()
			temp = self.temp.value()
			angle1 = self.angle1.value()
			angle2 = self.angle2.value()
			fuel = self.fuel.value()
			with open('data.txt', 'w') as file:
				file.write('{},{},{},{},{},{}'.format(speed,rpm,temp,angle1,angle2,fuel))
			time.sleep(.01)


def main():
	app = QApplication(sys.argv)        # start PyQT
	window = MainApp()
	#window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
	window.show()
	app.exec_()

if __name__ == '__main__':              # run PyQT
	main()
