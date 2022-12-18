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

qtCreatorFile = "untitled.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MainApp(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self, parent=None):
		super(MainApp, self).__init__(parent)
		QMainWindow.__init__(self)
		self.setupUi(self)
		print(QStyleFactory.keys())
		
		self.setStyle(QStyleFactory.create('Breeze'))
		self.setStyleSheet("QMainWindow {background: rgb(35,35,35);}")
		self.insideTemp.setStyleSheet('color: white')
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
		
def main():
	app = QApplication(sys.argv)        # start PyQT
	window = MainApp()
	window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
	window.show()
	app.exec_()

if __name__ == '__main__':              # run PyQT
	main()
