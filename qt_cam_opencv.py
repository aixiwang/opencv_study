# -*- coding: utf-8 -*-
#Importing necessary libraries, mainly the OpenCV, and PyQt libraries
import cv2
import numpy as np
import sys
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal

 
def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
    # return the edged image
    return edged
    

class ShowVideo(QtCore.QObject):

    #initiating the built in camera
    camera_port = 0
    camera = cv2.VideoCapture(camera_port)
    VideoSignal = QtCore.pyqtSignal(QtGui.QImage)

    def __init__(self, parent = None):
        super(ShowVideo, self).__init__(parent)

    @QtCore.pyqtSlot()
    def startVideo(self):
        run_video = True
        while run_video:
            ret, image = self.camera.read()
            #image2 = auto_canny(image)
            #image3 = cv2.cvtColor(image2,cv2.COLOR_GRAY2RGB)
            color_swapped_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            height, width, _ = color_swapped_image.shape

            qt_image = QtGui.QImage(color_swapped_image.data,
                                    width, 
                                    height,
                                    color_swapped_image.strides[0],
                                    QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap(qt_image)
            qt_image = pixmap.scaled(1280, 1024, QtCore.Qt.KeepAspectRatio)
            qt_image = QtGui.QImage(qt_image)

            self.VideoSignal.emit(qt_image)

class ImageViewer(QtWidgets.QWidget):
	def __init__(self, parent = None):
		super(ImageViewer, self).__init__(parent)
		self.image = QtGui.QImage()
		self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)



	def paintEvent(self, event):
		painter = QtGui.QPainter(self)
		painter.drawImage(0,0, self.image)
		self.image = QtGui.QImage()

	def initUI(self):
		self.setWindowTitle('Test')

	
	@QtCore.pyqtSlot(QtGui.QImage)
	def setImage(self, image):
		if image.isNull():
			print("viewer dropped frame!")

		self.image = image
		if image.size() != self.size():
			self.setFixedSize(image.size())
		self.update()


if __name__ == '__main__':

	app = QtWidgets.QApplication(sys.argv)
	thread = QtCore.QThread()
	thread.start()

	vid = ShowVideo()
	vid.moveToThread(thread)
	image_viewer = ImageViewer()
	#image_viewer.resize(200,400)
	

	vid.VideoSignal.connect(image_viewer.setImage)

	#Button to start the videocapture:

	push_button = QtWidgets.QPushButton('Start')
	push_button.clicked.connect(vid.startVideo)
	vertical_layout = QtWidgets.QVBoxLayout()

	vertical_layout.addWidget(image_viewer)
	vertical_layout.addWidget(push_button)

	layout_widget = QtWidgets.QWidget()
	layout_widget.setLayout(vertical_layout)

	main_window = QtWidgets.QMainWindow()
	main_window.setCentralWidget(layout_widget)
	main_window.resize(1280,1024)
	main_window.show()
	sys.exit(app.exec_())