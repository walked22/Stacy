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

color = QColor(61, 174, 233)

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

seatbelt = 0
batt = 0
engine = 0
highs = 0
lights = 0
oil = 0
fourWheel = 0
fourLow = 0
brake = 0
left = 0
right = 0

class mainthread(QThread):
	speedSignal = pyqtSignal('PyQt_PyObject')
	rpmSignal = pyqtSignal('PyQt_PyObject')
	angle1Signal = pyqtSignal('PyQt_PyObject')
	angle2Signal = pyqtSignal('PyQt_PyObject')
	tempSignal = pyqtSignal('PyQt_PyObject')
	fuelSignal = pyqtSignal('PyQt_PyObject')
	warningSignal = pyqtSignal('PyQt_PyObject')

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

					self.warningSignal.emit(data[6:])
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
		self.setStyleSheet("QMainWindow {background: rgb(0,0,0);}")
		self._margins = 10
		self.speeds = {0: "0", 30: "15", 60: "30", 90: "45", 120: "60", 150: "75", 180: "90", 210: "105", 240: "120"}
		self.rpms = {0: '0', 30: '1', 60: '2', 90: '3', 120: '4', 150: '5', 180: '6', 210: '7'}
		self.mythread1.speedSignal.connect(self.updateSpeed)
		self.mythread1.rpmSignal.connect(self.updateRPM)
		self.mythread1.tempSignal.connect(self.updateTemp)
		self.mythread1.angle1Signal.connect(self.updateAngle1)
		self.mythread1.angle2Signal.connect(self.updateAngle2)
		self.mythread1.fuelSignal.connect(self.updateFuel)
		self.mythread1.warningSignal.connect(self.updateWarning)

	def updateSpeed(self, s):
		global speed
		global color
		try:
			speed = int(s)
			if 68.3 <= speed <= 69.7:
				color = QColor(255,20,147)
			else:
				color = QColor(61, 174, 233)
			#print(speed)
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

	def updateWarning(self, W):
		global seatbelt
		global batt
		global engine
		global highs
		global oil
		global fourWheel
		global fourLow
		global brake
		global left
		global right
		try:
			seatbelt = int(W[0])
			batt = int(W[1])
			engine = int(W[2])
			highs = int(W[3])
			oil = int(W[4])
			fourWheel = int(W[5])
			fourLow = int(W[6])
			brake = int(W[7])
			left = int(W[8])
			right = int(W[9])
		except:
			pass

	def paintEvent(self, event):
		painter = QPainter()
		painter.begin(self)
		painter.setRenderHint(QPainter.Antialiasing)

		painter.fillRect(event.rect(), self.palette().brush(QPalette.Window))

		self.drawSpeed(painter)
		self.drawSpeedLines(painter)
		self.drawSpeedNumbers(painter)
		#self.drawSpeedNeedle(painter)

		self.drawRPMLines(painter)
		#self.drawRPMNeedle(painter)
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

		self.drawWarnings(painter)

		painter.end()

################################------Speed------##########################################

	def drawSpeedLines(self, painter):
		global speed
		global r1
		global z1
		painter.save()
		painter.translate(self.width()/4, self.height()/2)
		scale = min((self.width() - self._margins)/120.0, (self.height() - self._margins)/120.0)
		painter.scale(scale*.75, scale*.75)
		#painter.drawArc(-50, -50, 100, 100, 30*16, 210*16-speed/z1*16)
		if speed <= 85:
			painter.setPen(color)
		else:
			painter.setPen(QColor(255, 0, 0))
		painter.drawArc(-50,-50,100,100, 240*16, -speed/z1*16)
		painter.restore()

	def drawSpeedNumbers(self, painter):
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
				painter.setPen(color)
			else:
				painter.setPen(QColor(255, 255, 255))
			painter.translate(math.cos(i*30*math.pi/180+x*math.pi/180)*59, math.sin(i*30*math.pi/180+x*math.pi/180)*59)
			if speed >= int(self.speeds[30*i]):
				painter.drawText(-metrics.width(self.speeds[30*i])/2, 3, self.speeds[30*i])
			painter.restore()
			i += 1

	def drawSpeedNeedle(self, painter):
		global speed
		global z1
		global r1
		painter.save()
		painter.translate(self.width()/4, self.height()/2)
		painter.rotate(speed/z1+r1)
		scale = min((self.width() - self._margins)/120.0,(self.height() - self._margins)/120.0)
		painter.scale(scale*.75, scale*.75)
		painter.setPen(QPen(Qt.NoPen))
		painter.setBrush(color)
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
				painter.setPen(color)
			else:
				painter.setPen(QColor(255, 255, 255))
			painter.translate(math.cos(i*30*math.pi/180+x*math.pi/180)*58, math.sin(i*30*math.pi/180+x*math.pi/180)*58)
			if rpm/1000 >= int(self.rpms[30*i]):
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
		#painter.drawArc(-50, -50, 100, 100, 30*16, 210*16-rpm/z*16)
		if rpm <= 4500:
			painter.setPen(color)
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
		painter.setBrush(color)
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
			painter.setPen(color)
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
			painter.setPen(color)
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
		painter.setBrush(color)
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
			painter.setPen(color)
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
		painter.setBrush(color)
		painter.drawPolygon(QPolygon([QPoint(-1, -54), QPoint(1, -54), QPoint(1, -46), QPoint(-1, -46)]))
		painter.restore()

################################------Warning Indicators------##########################################
	
	def drawWarnings(self, painter):
		global seatbelt
		global batt
		global engine
		global highs
		global lights
		global oil
		global fourWheel
		global fourLow
		global brake
		global left
		global right
		painter.save()
		sb_pic = QPixmap("seatbelt.png")
		oil_pic = QPixmap("oil.png")
		batt_pic = QPixmap("batt.png")
		highs_pic = QPixmap("highs.png")
		left_pic = QPixmap("left.png")
		right_pic = QPixmap("right.png")
		font = QFont(self.font())
		font.setPixelSize(14)
		metrics = QFontMetricsF(font)
		painter.translate(self.width()*.30, self.height()*.03)
		painter.scale(.15,.15)
		if seatbelt == 1:
			painter.drawPixmap(0, 0, sb_pic)
		#painter.drawText(QRectF(135,75,60,40), Qt.AlignCenter, str(angle2)+u"\u00b0")
		if batt == 1:
			painter.resetTransform()
			painter.translate(self.width()*.5-50, self.height()*.03)
			painter.scale(.08,.08)
			painter.drawPixmap(self.rect(), batt_pic)
		if oil == 1:
			painter.resetTransform()
			painter.translate(self.width()*.7-50, self.height()*.03)
			painter.scale(.1,.08)
			painter.drawPixmap(self.rect(), oil_pic)
		if engine == 1:
			painter.setPen(QColor(255, 0, 0))
			font.setBold(1)
			painter.setFont(font)
			painter.resetTransform()
			painter.translate(self.width()/4-5, self.height()/3)
			painter.drawText(-metrics.width('CHECK')/2, 3, 'CHECK')
			painter.translate(0,15)
			painter.drawText(-metrics.width('ENGINE')/2, 3, 'ENGINE')
		if fourWheel == 1:
			painter.setPen(color)
			font.setBold(1)
			font.setPixelSize(20)
			painter.setFont(font)
			painter.resetTransform()
			painter.translate(self.width()*.75-13, self.height()/3)
			painter.drawText(-metrics.width('4WD')/2, 3, '4WD')
		if fourLow == 1:
			painter.resetTransform()
			painter.setPen(color)
			font.setBold(1)
			font.setPixelSize(20)
			painter.setFont(font)
			painter.translate(self.width()*.75+30, self.height()/3)
			painter.drawText(-metrics.width('-L')/2, 3, '-L')
		if brake == 1:
			painter.resetTransform()
			painter.setPen(QColor(255, 0, 0))
			font.setBold(1)
			font.setPixelSize(20)
			painter.setFont(font)
			painter.translate(self.width()/2-metrics.width('BRAKE')/2, self.height()*.75)
			painter.drawText(-metrics.width('BRAKE')/2, 3, 'BRAKE')
		if highs == 1:
			painter.resetTransform()
			painter.translate(self.width()*.5-40, self.height()*.17)
			painter.scale(.06,.06)
			painter.drawPixmap(self.rect(), highs_pic)
		if left == 1:
			painter.resetTransform()
			painter.translate(self.width()*.2-140, self.height()*.84)
			painter.scale(.15, .15)
			painter.drawPixmap(self.rect(), left_pic)
		if right == 1:
			painter.resetTransform()
			painter.translate(self.width()*.8, self.height()*.84)
			painter.scale(.15,.15)
			painter.drawPixmap(self.rect(), right_pic)
		painter.restore()



def main():
	app = QApplication(sys.argv)        # start PyQT
	window = MainApp()
	#window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
	window.show()
	app.exec_()

if __name__ == '__main__':              # run PyQT
	main()
