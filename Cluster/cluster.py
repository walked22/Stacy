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
z = 100/3
speed = 0
rpm = 0
temp =0
fuel = 0
angle1 = 0
angle2 = 0
z1 = .5
ztemp = .75
zfuel = .9

class mainthread(QThread):
	speedSignal = pyqtSignal('PyQt_PyObject')
	rpmSignal = pyqtSignal('PyQt_PyObject')
	angle1Signal = pyqtSignal('PyQt_PyObject')
	angle2Signal = pyqtSignal('PyQt_PyObject')
	tempSignal = pyqtSignal('PyQt_PyObject')
	fuelSignal = pyqtSignal('PyQt_PyObject')

	def __init__(self):                                            # PyQT initialization function
		QThread.__init__(self)

	def __del__(self):
		self.wait()

	def run(self):
		while True:
			with open('data.txt', 'r') as file:
				data = file.read().split(',')
				try:
					self.speedSignal.emit(data[0])
					self.rpmSignal.emit(data[1])
					self.tempSignal.emit(data[2])
					self.angle1Signal.emit(data[3])
					self.angle2Signal.emit(data[4])
					self.fuelSignal.emit(data[5])
				except:
					pass

class MainApp(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self, parent=None):
		super(MainApp, self).__init__(parent)
		QMainWindow.__init__(self)
		self.setupUi(self)
		self.mythread1 = mainthread()
		self.mythread1.start()
		self.setStyle(QStyleFactory.create('breeze'))
		self.setStyleSheet("QMainWindow {background: rgb(35,35,35);}")
		self._margins = 10
		self.speeds = {0: "0", 30: "15", 60: "30", 90: "45", 120: "60", 150: "75", 180: "90", 210: "105", 240: "120"}
		self.rpms = {0: '0', 30: '1', 60: '2', 90: '3', 120: '4', 150: '5', 180: '6', 210: '7'}
		self.mythread1.speedSignal.connect(self.updateSpeed)
		self.mythread1.rpmSignal.connect(self.updateRPM)
		self.mythread1.tempSignal.connect(self.updateTemp)
		self.mythread1.angle1Signal.connect(self.updateAngle1)
		self.mythread1.angle2Signal.connect(self.updateAngle2)
		self.mythread1.fuelSignal.connect(self.updateFuel)

	def updateSpeed(self, s):
		global speed
		try:
			speed = int(s)
			print(speed)
			self.update()
		except:
			pass

	def updateRPM(self, r):
		global rpm
		try:
			rpm = int(r)
		except:
			pass

	def updateAngle1(self, a1):
		global angle1
		try:
			angle1 = int(a1)
		except:
			pass

	def updateAngle2(self, a2):
		global angle2
		try:
			angle2 = int(a2)
		except:
			pass

	def updateTemp(self, T):
		global temp
		try:
			temp = int(T)
		except:
			pass

	def updateFuel(self, F):
		global fuel
		try:
			fuel = int(F)
		except:
			pass

	def paintEvent(self, event):
		painter = QPainter()
		painter.begin(self)
		painter.setRenderHint(QPainter.Antialiasing)

		painter.fillRect(event.rect(), self.palette().brush(QPalette.Window))

		#self.drawSpeedLines(painter)
		self.drawSpeed(painter)
		#self.drawSpeedNumbers(painter)
		self.drawSpeedLinesSimple(painter)
		self.drawSpeedNumbersSimple(painter)
		#self.drawSpeedNeedle(painter)
		self.drawSpeedNeedleSimple(painter)

		self.drawRPMLines(painter)
		self.drawRPMNeedle(painter)
		self.drawRPM(painter)
		self.drawRPMNumbers(painter)

		self.drawCar(painter)
		self.drawCarBack(painter)

		self.drawTempLines(painter)
		self.drawTempMarks(painter)
		self.drawTempNeedle(painter)

		self.drawFuelLines(painter)
		self.drawFuelMarks(painter)
		self.drawFuelNeedle(painter)

		painter.end()

################################------Speed------##########################################

	def drawSpeedNumbers(self, painter):
		global speed
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
			if speed*2-6 <= i*30 and speed*2+6 >= i*30:
				painter.setPen(QColor(61, 174, 233))
			else:
				painter.setPen(QColor(255, 255, 255))
			painter.translate(math.cos(i*30*math.pi/180+x*math.pi/180)*60, math.sin(i*30*math.pi/180+x*math.pi/180)*60)
			painter.drawText(-metrics.width(self.speeds[30*i])/2, 3, self.speeds[30*i])
			painter.restore()
			i += 1

	def drawSpeedLines(self, painter):
		global speed
		global r
		painter.save()
		painter.translate(self.width()/4, self.height()/2)
		scale = min((self.width() - self._margins)/120.0, (self.height() - self._margins)/120.0)
		painter.scale(scale*.75, scale*.75)
		painter.rotate(r)
		i = 0
		while i < 241:
			if i % 30 == 0:
				if speed*2+6 >= i:
					painter.setPen(QColor(61, 174, 233))
				else:
					painter.setPen(QColor(255, 255, 255))
				painter.drawLine(0, -40, 0, -50)
			else:
				if speed >= 85:
					painter.setPen(QColor(255, 0, 0))
				else:
					if speed*2+6 >= i:
						painter.setPen(QColor(67, 174, 233))
					else:
						painter.setPen(QColor(255, 255, 255))
				painter.drawLine(0, -45, 0, -50)
			painter.rotate(7.5)
			i += 7.5
		painter.restore()

	def drawSpeedLinesSimple(self, painter):
		global speed
		global r1
		global z1
		painter.save()
		painter.translate(self.width()/4, self.height()/2)
		scale = min((self.width() - self._margins)/120.0, (self.height() - self._margins)/120.0)
		painter.scale(scale*.75, scale*.75)
		painter.drawArc(-50, -50, 100, 100, 30*16, 210*16-speed/z1*16)
		if speed <= 85:
			painter.setPen(QColor(61, 174, 233))
		else:
			painter.setPen(QColor(255, 0, 0))
		painter.drawArc(-50,-50,100,100, 240*16, -speed/z1*16)
		painter.restore()

	def drawSpeedNumbersSimple(self, painter):
		global speed
		global z1
		x = -240
		i = 0 
		while i < 8:
			painter.save()
			painter.translate(self.width()/4, self.height()/2)
			scale = min((self.width() - self._margins)/120.0, (self.height() - self._margins)/120.0)
			painter.scale(scale*.75, scale*.75)
			font = QFont(self.font())
			font.setPixelSize(8)
			metrics = QFontMetricsF(font)
			painter.setFont(font)
			if speed/z1-6 <= i*30 and speed/z1+6 >= i*30:
				painter.setPen(QColor(61, 174, 233))
			else:
				painter.setPen(QColor(255, 255, 255))
			painter.translate(math.cos(i*30*math.pi/180+x*math.pi/180)*59, math.sin(i*30*math.pi/180+x*math.pi/180)*59)
			painter.drawText(-metrics.width(self.speeds[30*i])/2, 3, self.speeds[30*i])
			painter.restore()
			i += 1

	def drawSpeedNeedleSimple(self, painter):
		global speed
		global z1
		global r1
		painter.save()
		painter.translate(self.width()/4, self.height()/2)
		painter.rotate(speed/z1+r1)
		scale = min((self.width() - self._margins)/120.0,(self.height() - self._margins)/120.0)
		painter.scale(scale*.75, scale*.75)
		painter.setPen(QPen(Qt.NoPen))
		painter.setBrush(QColor(61, 174, 233))
		painter.drawPolygon(QPolygon([QPoint(-1, -54), QPoint(1, -54), QPoint(1, -46), QPoint(-1, -46)]))
		painter.restore()

	def drawSpeed(self, painter):
		painter.save()
		painter.translate(self.width()/4, self.height()/2)
		scale = min((self.width() - self._margins)/120.0,(self.height() - self._margins)/120.0)
		painter.scale(scale*.75, scale*.75)
		font = QFont(self.font())
		font.setPixelSize(12)
		metrics = QFontMetricsF(font)
		painter.setFont(font)
		if speed >= 85:
			painter.setPen(QColor(255, 0, 0))
		else:
			painter.setPen(QColor(67, 174, 233))
		painter.drawText(QRectF(-20,-10,40,20), Qt.AlignCenter, str(speed))
		font.setPixelSize(6)
		font.setItalic(1)
		painter.setFont(font)
		painter.drawText(QRectF(-20,2,40,20), Qt.AlignCenter, 'MPH')
		painter.restore()

	def drawSpeedNeedle(self, painter):
		global r
		global speed
		if isinstance(speed, int):
			painter.save()
			painter.translate(self.width()/4, self.height()/2)
			painter.rotate(speed*2+r)
			scale = min((self.width() - self._margins)/120.0,(self.height() - self._margins)/120.0)
			painter.scale(scale*.75, scale*.75)
			painter.setPen(QPen(Qt.NoPen))
			painter.setBrush(QColor(255, 255, 255))
			painter.drawPolygon(QPolygon([QPoint(-3, 0), QPoint(0, -35), QPoint(3, 0), QPoint(0, 15), QPoint(-3, 0)]))
			painter.setBrush(QColor(61, 174, 233))
			painter.drawPolygon(QPolygon([QPoint(-1.5, -25), QPoint(0, -35), QPoint(1.5, -25), QPoint(-1.5, -25)]))
			painter.restore()


################################------RPM------##########################################

	def drawRPMNumbers(self, painter):
		global rpm
		global z
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
			if rpm/z-6 <= i*30 and rpm/z+6 >= i*30:
				painter.setPen(QColor(61, 174, 233))
			else:
				painter.setPen(QColor(255, 255, 255))
			painter.translate(math.cos(i*30*math.pi/180+x*math.pi/180)*58, math.sin(i*30*math.pi/180+x*math.pi/180)*58)
			painter.drawText(-metrics.width(self.rpms[30*i])/2, 3, self.rpms[30*i])
			painter.restore()
			i += 1

	def drawRPMLines(self, painter):
		global rpm
		global r1
		global z
		painter.save()
		painter.translate(self.width()*.75, self.height()/2)
		scale = min((self.width() - self._margins)/120.0, (self.height() - self._margins)/120.0)
		painter.scale(scale*.75, scale*.75)
		painter.drawArc(-50, -50, 100, 100, 30*16, 210*16-rpm/z*16)
		if rpm <= 4500:
			painter.setPen(QColor(61, 174, 233))
		else:
			painter.setPen(QColor(255, 0, 0))
		painter.drawArc(-50,-50,100,100, 240*16, -rpm/z*16)
		painter.restore()

	def drawRPMNeedle(self, painter):
		global rpm
		global r1
		global z
		painter.save()
		painter.translate(self.width()*.75, self.height()/2)
		painter.rotate(rpm/z+r1)
		scale = min((self.width() - self._margins)/120.0,(self.height() - self._margins)/120.0)
		painter.scale(scale*.75, scale*.75)
		painter.setPen(QPen(Qt.NoPen))
		painter.setBrush(QColor(61, 174, 233))
		painter.drawPolygon(QPolygon([QPoint(-1, -54), QPoint(1, -54), QPoint(1, -46), QPoint(-1, -46)]))
		painter.restore()

	def drawRPM(self, painter):
		global rpm
		painter.save()
		painter.translate(self.width()*.75, self.height()/2)
		scale = min((self.width() - self._margins)/120.0,(self.height() - self._margins)/120.0)
		painter.scale(scale*.75, scale*.75)
		font = QFont(self.font())
		font.setPixelSize(12)
		metrics = QFontMetricsF(font)
		painter.setFont(font)
		if rpm <= 4500:
			painter.setPen(QColor(61, 174, 233))
		else:
			painter.setPen(QColor(255, 0, 0))
		painter.drawText(QRectF(-20,-10,40,20), Qt.AlignCenter, str(rpm))
		font.setPixelSize(6)
		font.setItalic(1)
		painter.setFont(font)
		painter.drawText(QRectF(-20,2,40,20), Qt.AlignCenter, 'RPM')
		painter.restore()

################################------CAR------##########################################

	def drawCar(self, painter):
		global angle1
		painter.save()
		pic = QPixmap("Geo.png")
		font = QFont(self.font())
		font.setPixelSize(30)
		metrics = QFontMetricsF(font)
		painter.setFont(font)
		painter.translate(self.width()*.5, self.height()*.85)
		painter.scale(.5,.5)
		painter.rotate(-angle1)
		painter.drawPixmap(0, 0, pic)
		painter.drawText(QRectF(85,25,60,40), Qt.AlignCenter, str(angle1)+u"\u00b0")
		painter.restore()

	def drawCarBack(self, painter):
		global angle2
		painter.save()
		pic = QPixmap("GeoBack.png")
		font = QFont(self.font())
		font.setPixelSize(50)
		metrics = QFontMetricsF(font)
		painter.setFont(font)
		painter.translate(self.width()*.35, self.height()*.85)
		painter.scale(.3,.3)
		painter.rotate(-angle2)
		painter.drawPixmap(0, 0, pic)
		painter.drawText(QRectF(135,75,60,40), Qt.AlignCenter, str(angle2)+u"\u00b0")
		painter.restore()

################################------Temp------##########################################

	def drawTempLines(self, painter):
		global temp
		global r1
		global ztemp
		painter.save()
		painter.translate(self.width()/4, self.height()/2)
		scale = min((self.width() - self._margins)/120.0, (self.height() - self._margins)/120.0)
		painter.scale(scale*.75, scale*.75)
		painter.setPen(QColor(255, 0, 0))
		painter.drawArc(-50, -50, 100, 100, -0*16, -90*16+temp*ztemp*16)
		if temp <= 100:
			painter.setPen(QColor(61, 174, 233))
		else:
			painter.setPen(QColor(255, 0, 0))
		painter.drawArc(-50,-50,100,100, -90*16, 0+temp*ztemp*16)
		painter.restore()

	def drawTempMarks(self, painter):
		global temp
		painter.save()
		painter.translate(self.width()/4, self.height()/2+230)
		font = QFont(self.font())
		font.setPixelSize(35)
		metrics = QFontMetricsF(font)
		font.setItalic(1)
		painter.setFont(font)
		painter.drawText(-metrics.width('C')/2, 3, 'C')
		painter.translate(215,-220)
		if temp >= 100:
			painter.setPen(QColor(255, 0, 0))
		else:
			painter.setPen(QColor(255, 255, 255))
		painter.drawText(-metrics.width('H')/2, 3, 'H')
		painter.restore()

	def drawTempNeedle(self, painter):
		global temp
		global ztemp
		painter.save()
		painter.translate(self.width()/4, self.height()/2)
		painter.rotate(-temp*ztemp+180)
		scale = min((self.width() - self._margins)/120.0,(self.height() - self._margins)/120.0)
		painter.scale(scale*.75, scale*.75)
		painter.setPen(QPen(Qt.NoPen))
		painter.setBrush(QColor(61, 174, 233))
		painter.drawPolygon(QPolygon([QPoint(-1, -54), QPoint(1, -54), QPoint(1, -46), QPoint(-1, -46)]))
		painter.restore()

################################------Fuel------##########################################

	def drawFuelLines(self, painter):
		global fuel
		global r1
		global zfuel
		painter.save()
		painter.translate(self.width()*.75, self.height()/2)
		scale = min((self.width() - self._margins)/120.0, (self.height() - self._margins)/120.0)
		painter.scale(scale*.75, scale*.75)
		painter.drawArc(-50, -50, 100, 100, -0*16, -90*16+fuel*zfuel*16)
		if fuel <= 20:
			painter.setPen(QColor(255, 0, 0))
		elif 20 < fuel <= 80:
			painter.setPen(QColor(61, 174, 233))
		else:
			painter.setPen(QColor(0, 255, 0))
		painter.drawArc(-50,-50,100,100, -90*16, 0+fuel*zfuel*16)
		painter.restore()

	def drawFuelMarks(self, painter):
		global fuel
		painter.save()
		painter.translate(self.width()*.75, self.height()/2+230)
		font = QFont(self.font())
		font.setPixelSize(35)
		metrics = QFontMetricsF(font)
		font.setItalic(1)
		painter.setFont(font)
		if fuel <= 20:
			painter.setPen(QColor(255, 0, 0))
		else:
			painter.setPen(QColor(255, 255, 255))
		painter.drawText(-metrics.width('E')/2, 3, 'E')
		painter.translate(215,-220)
		if 20 < fuel <= 80:
			painter.setPen(QColor(255, 255, 255))
		elif fuel > 80:
			painter.setPen(QColor(0, 255, 0))
		else:
			painter.setPen(QColor(255, 255, 255))
		painter.drawText(-metrics.width('F')/2, 3, 'F')
		painter.restore()

	def drawFuelNeedle(self, painter):
		global fuel
		global zfuel
		painter.save()
		painter.translate(self.width()*.75, self.height()/2)
		painter.rotate(-fuel*zfuel+180)
		scale = min((self.width() - self._margins)/120.0,(self.height() - self._margins)/120.0)
		painter.scale(scale*.75, scale*.75)
		painter.setPen(QPen(Qt.NoPen))
		painter.setBrush(QColor(61, 174, 233))
		painter.drawPolygon(QPolygon([QPoint(-1, -54), QPoint(1, -54), QPoint(1, -46), QPoint(-1, -46)]))
		painter.restore()

def main():
	app = QApplication(sys.argv)        # start PyQT
	window = MainApp()
	#window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
	window.show()
	app.exec_()

if __name__ == '__main__':              # run PyQT
	main()
