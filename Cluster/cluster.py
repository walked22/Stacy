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

qtCreatorFile = "speed.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

r = -120
r1 = -150

class MainApp(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self, parent=None):
		super(MainApp, self).__init__(parent)
		QMainWindow.__init__(self)
		self.setupUi(self)
		self.setStyle(QStyleFactory.create('breeze'))
		self.setStyleSheet("QMainWindow {background: rgb(35,35,35);}")
		self._margins = 10
		self.speeds = {0: "0", 30: "15", 60: "30", 90: "45", 120: "60", 150: "75", 180: "90", 210: "105", 240: "120"}
		self.rpms = {0: '0', 30: '1', 60: '2', 90: '3', 120: '4', 150: '5', 180: '6', 210: '7'}
		self.dial.valueChanged.connect(self.update)
		self.dial1.valueChanged.connect(self.update)

	def paintEvent(self, event):
		painter = QPainter()
		painter.begin(self)
		painter.setRenderHint(QPainter.Antialiasing)

		painter.fillRect(event.rect(), self.palette().brush(QPalette.Window))
		self.drawSpeedLines(painter)
		self.drawSpeedNeedle(painter)
		self.drawRPMLines(painter)
		self.drawRPMNeedle(painter)
		self.drawSpeedNumber(painter)
		self.drawCar(painter)
		self.drawAngle(painter)
		self.drawSpeedNumbers(painter)
		self.drawRPMNumbers(painter)


		painter.end()

	def drawSpeedNumbers(self, painter):
		x = -210
		i = 0 
		while i < 9:
			painter.save()
			painter.translate(self.width()/4, self.height()/2)
			scale = min((self.width() - self._margins)/120.0, (self.height() - self._margins)/120.0)
			painter.scale(scale*.75, scale*.75)
			font = QFont(self.font())
			font.setPixelSize(8)
			metrics = QFontMetricsF(font)
			painter.setFont(font)
			if self.dial.value()*2-6 <= i*30 and self.dial.value()*2+6 >= i*30:
				painter.setPen(QColor(61, 174, 233))
			else:
				painter.setPen(QColor(255, 255, 255))
			painter.translate(math.cos(i*30*math.pi/180+x*math.pi/180)*58, math.sin(i*30*math.pi/180+x*math.pi/180)*58)
			painter.drawText(-metrics.width(self.speeds[30*i])/2, 3, self.speeds[30*i])
			painter.restore()
			i += 1

	def drawSpeedLines(self, painter):
		global r
		painter.save()
		painter.translate(self.width()/4, self.height()/2)
		scale = min((self.width() - self._margins)/120.0, (self.height() - self._margins)/120.0)
		painter.scale(scale*.75, scale*.75)
		painter.rotate(r)
		i = 0
		while i < 241:
			if i % 30 == 0:
				if self.dial.value()*2+6 >= i:
					painter.setPen(QColor(61, 174, 233))
				else:
					painter.setPen(QColor(255, 255, 255))
				painter.drawLine(0, -40, 0, -50)
			else:
				if self.dial.value() >= 85:
					painter.setPen(QColor(255, 0, 0))
				else:
					if self.dial.value()*2+6 >= i:
						painter.setPen(QColor(67, 174, 233))
					else:
						painter.setPen(QColor(255, 255, 255))
				painter.drawLine(0, -45, 0, -50)
			painter.rotate(7.5)
			i += 7.5
		painter.restore()

	def drawSpeedNumber(self, painter):
		painter.save()
		painter.translate(self.width()/4, self.height()/2)
		font = QFont(self.font())
		font.setPixelSize(20)
		metrics = QFontMetricsF(font)
		painter.setFont(font)
		if self.dial.value() >= 85:
			painter.setPen(QColor(255, 0, 0))
		else:
			painter.setPen(QColor(255,255,255))
		painter.drawText(QRectF(-20,60,40,20), Qt.AlignCenter, str(self.dial.value()))
		painter.restore()

	def drawSpeedNeedle(self, painter):
		global r
		painter.save()
		painter.translate(self.width()/4, self.height()/2)
		painter.rotate(self.dial.value()*2+r)
		scale = min((self.width() - self._margins)/120.0,(self.height() - self._margins)/120.0)
		painter.scale(scale*.75, scale*.75)

		painter.setPen(QPen(Qt.NoPen))
		painter.setBrush(QColor(255, 255, 255))

		painter.drawPolygon(QPolygon([QPoint(-3, 0), QPoint(0, -35), QPoint(3, 0), QPoint(0, 15), QPoint(-3, 0)]))

		painter.setBrush(QColor(61, 174, 233))

		painter.drawPolygon(QPolygon([QPoint(-1.5, -25), QPoint(0, -35), QPoint(1.5, -25), QPoint(-1.5, -25)]))

		painter.restore()

	def drawRPMNumbers(self, painter):
		x = -240
		i = 0 
		while i < 8:
			painter.save()
			painter.translate(self.width()*.75, self.height()/2)
			scale = min((self.width() - self._margins)/120.0, (self.height() - self._margins)/120.0)
			painter.scale(scale*.75, scale*.75)
			font = QFont(self.font())
			font.setPixelSize(8)
			metrics = QFontMetricsF(font)
			painter.setFont(font)
			if self.dial1.value()*30-6 <= i*30 and self.dial1.value()*30+6 >= i*30:
				painter.setPen(QColor(61, 174, 233))
			else:
				painter.setPen(QColor(255, 255, 255))
			painter.translate(math.cos(i*30*math.pi/180+x*math.pi/180)*58, math.sin(i*30*math.pi/180+x*math.pi/180)*58)
			painter.drawText(-metrics.width(self.rpms[30*i])/2, 3, self.rpms[30*i])
			painter.restore()
			i += 1

	def drawRPMLines(self, painter):
		global r1
		painter.save()
		painter.translate(self.width()*.75, self.height()/2)
		scale = min((self.width() - self._margins)/120.0, (self.height() - self._margins)/120.0)
		painter.scale(scale*.75, scale*.75)
		painter.rotate(r1)
		i = 0
		while i < 211:
			if i % 30 == 0:
				if self.dial1.value()*30+6 >= i:
					painter.setPen(QColor(61, 174, 233))
				else:
					painter.setPen(QColor(255, 255, 255))
				painter.drawLine(0, -40, 0, -50)
			else:
				if self.dial1.value() >= 4:
					painter.setPen(QColor(255, 0, 0))
				else:
					if self.dial1.value()*30+6 >= i:
						painter.setPen(QColor(67, 174, 233))
					else:
						painter.setPen(QColor(255, 255, 255))
				painter.drawLine(0, -45, 0, -50)
			painter.rotate(7.5)
			i += 7.5
		painter.restore()

	def drawRPMNeedle(self, painter):
		global r1
		painter.save()
		painter.translate(self.width()*.75, self.height()/2)
		painter.rotate(self.dial1.value()*30+r1)
		scale = min((self.width() - self._margins)/120.0,(self.height() - self._margins)/120.0)
		painter.scale(scale*.75, scale*.75)

		painter.setPen(QPen(Qt.NoPen))
		painter.setBrush(QColor(255, 255, 255))

		painter.drawPolygon(QPolygon([QPoint(-3, 0), QPoint(0, -35), QPoint(3, 0), QPoint(0, 15), QPoint(-3, 0)]))

		painter.setBrush(QColor(61, 174, 233))

		painter.drawPolygon(QPolygon([QPoint(-1.5, -25), QPoint(0, -35), QPoint(1.5, -25), QPoint(-1.5, -25)]))

		painter.restore()



	def drawCar(self, painter):
		painter.save()
		pic = QPixmap("Geo.png")
		painter.scale(.1,.1)
		painter.translate(self.width()*8, self.height()*8)
		painter.rotate(self.dial.value())
		painter.drawPixmap(self.rect(), pic)
		painter.restore()

	def drawAngle(self, painter):
		painter.save()
		painter.translate(self.width()*.8, self.height()*.9)
		painter.setPen(QColor(255,255,255))
		#painter.setBrush(QColor(255, 0, 0))
		painter.drawLine(0,0,100,0)
		painter.restore()

def main():
	app = QApplication(sys.argv)        # start PyQT
	window = MainApp()
	#window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
	window.show()
	app.exec_()

if __name__ == '__main__':              # run PyQT
	main()
