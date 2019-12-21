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

qtCreatorFile = "speed.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

r = 237

class MainApp(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self, parent=None):
		super(MainApp, self).__init__(parent)
		QMainWindow.__init__(self)
		self.setupUi(self)
		self.setStyle(QStyleFactory.create('breeze'))
		self.setStyleSheet("QMainWindow {background: rgb(35,35,35);}")
		self._margins = 10
		self._pointText = {0: "0", 30: "15", 60: "30", 90: "45", 120: "60",150: "75", 180: "90", 210: "105", 240: "120"}
		self.dial.valueChanged.connect(self.update)

#	def paintEvent(self, event):
#		painter = QPainter(self)
#		painter.setPen(QPen(Qt.black,  5, Qt.SolidLine))
#		painter.rotate(self.dial.value())
#		painter.drawRect(40, 40, 400, 200)

	def paintEvent(self, event):
		painter = QPainter()
		painter.begin(self)
		painter.setRenderHint(QPainter.Antialiasing)

		painter.fillRect(event.rect(), self.palette().brush(QPalette.Window))
		self.drawSpeed(painter)
		self.drawSpeedNeedle(painter)
		self.drawRPM(painter)
		self.drawRPMNeedle(painter)
		self.drawNumber(painter)

		painter.end()

	def drawSpeed(self, painter):
		global r
		painter.save()
		painter.translate(self.width()/4, self.height()/2)
		scale = min((self.width() - self._margins)/120.0, (self.height() - self._margins)/120.0)
		painter.scale(scale/2, scale/2)

		font = QFont(self.font())
		font.setPixelSize(10)
		metrics = QFontMetricsF(font)

		painter.setFont(font)

		painter.rotate(r)
		i = 0
		while i < 241:
			if i % 30 == 0:
				if self.dial.value()*2-6 <= i and self.dial.value()*2+6 >= i:
					painter.setPen(self.palette().color(QPalette.Highlight))
				else:
					painter.setPen(QColor(255, 255, 255))
				painter.drawLine(0, -40, 0, -50)
				painter.drawText(-metrics.width(self._pointText[i])/2.0, -52, self._pointText[i])
			else:
				if self.dial.value() >= 85:
					painter.setPen(QColor(255, 0, 0))
				else:
					painter.setPen(self.palette().color(QPalette.Shadow))
				painter.drawLine(0, -45, 0, -50)
			painter.rotate(7.5)
			i += 7.5
		painter.restore()

	def drawNumber(self, painter):
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
		painter.scale(scale/2, scale/2)

		painter.setPen(QPen(Qt.NoPen))
		painter.setBrush(self.palette().brush(QPalette.Shadow))

		painter.drawPolygon(QPolygon([QPoint(-3, 0), QPoint(0, -35), QPoint(3, 0), QPoint(0, 15), QPoint(-3, 0)]))

		painter.setBrush(self.palette().brush(QPalette.Highlight))

		painter.drawPolygon(QPolygon([QPoint(-1.5, -25), QPoint(0, -35), QPoint(1.5, -25), QPoint(-1.5, -25)]))

		painter.restore()


	def drawRPM(self, painter):
		painter.save()
		painter.translate(self.width()*.75, self.height()/2)
		scale = min((self.width() - self._margins)/120.0, (self.height() - self._margins)/120.0)
		painter.scale(scale/2, scale/2)

		font = QFont(self.font())
		font.setPixelSize(10)
		metrics = QFontMetricsF(font)

		painter.setFont(font)
		painter.setPen(self.palette().color(QPalette.Shadow))

		i = 0
		while i < 241:
			if i % 30 == 0:
				painter.drawLine(0, -40, 0, -50)
				painter.drawText(-metrics.width(self._pointText[i])/2.0, -52, self._pointText[i])
			else:
				painter.drawLine(0, -45, 0, -50)
			painter.rotate(15)
			i += 15
		painter.restore()

	def drawRPMNeedle(self, painter):
		painter.save()
		painter.translate(self.width()*.75, self.height()/2)
		painter.rotate(self.dial.value())
		scale = min((self.width() - self._margins)/120.0,(self.height() - self._margins)/120.0)
		painter.scale(scale/2, scale/2)

		painter.setPen(QPen(Qt.NoPen))
		painter.setBrush(self.palette().brush(QPalette.Shadow))

		painter.drawPolygon(QPolygon([QPoint(-10, 0), QPoint(0, -45), QPoint(10, 0),QPoint(0, 45), QPoint(-10, 0)]))

		painter.setBrush(self.palette().brush(QPalette.Highlight))

		painter.drawPolygon(QPolygon([QPoint(-5, -25), QPoint(0, -45), QPoint(5, -25),QPoint(0, -30), QPoint(-5, -25)]))

		painter.restore()


def main():
	app = QApplication(sys.argv)        # start PyQT
	window = MainApp()
	#window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
	window.show()
	app.exec_()

if __name__ == '__main__':              # run PyQT
	main()
