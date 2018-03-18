# -*- coding: utf-8 -*-


import numpy
import cv2
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys,time,os

count = 0

def mat2qpixmap(img):
    height,width = img.shape[:2]
    if img.ndim == 3:
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    elif img.ndim == 2:
        rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    else:
        raise Exception("unstatistified image data format!")
    #qimage = QImage(rgb.flatten(), width, height, QImage.Format_RGB888)
    qimage = QImage(rgb,width,height,img.ndim*width,QImage.Format_RGB888)
    qpixmap = QPixmap.fromImage(qimage)

    return qpixmap
    

class MyDialog(QDialog):
    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)

        self.cvImage = cv2.imread('meter.bmp')
        height, width, byteValue = self.cvImage.shape
        byteValue = byteValue * width

        cv2.cvtColor(self.cvImage, cv2.COLOR_BGR2RGB, self.cvImage)

        self.mQImage = QImage(self.cvImage, width, height, byteValue, QImage.Format_RGB888)
        self.initUI()
        
    def paintEvent(self, QPaintEvent):
        painter = QPainter()
        painter.begin(self)
        painter.drawImage(0, 0, self.mQImage)
        painter.end()

    def keyPressEvent(self, QKeyEvent):
        super(MyDialog, self).keyPressEvent(QKeyEvent)
        if 's' == QKeyEvent.text():
            cv2.imwrite("cat2.png", self.cvImage)
        elif 'd' == QKeyEvent.text():
            self.showDialog()
            
        else:
            app.exit(1)

            
    def initUI(self):      

        self.btn = QPushButton(r'上阈值', self)
        self.btn.move(320, 20)
        self.btn.clicked.connect(self.showDialog)
        
        self.le = QLineEdit(self)
        self.le.move(430, 22)
        
        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('模具保护器')
        self.show()
        
        
    def showDialog(self):
        
        text, ok = QInputDialog.getText(self, '上阈值', 
            'value:')
        
        if ok:
            self.le.setText(str(text))
           

    def initUI2(self):      

        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()

        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)       
        
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('File dialog')
        self.show()
        
        
    def showDialog2(self):

        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')

        if fname[0]:
            f = open(fname[0], 'r')

            with f:
                data = f.read()
                self.textEdit.setText(data)            

                
    def timer_hook(self):
        global count
        count = count + 1 
        print(count)
    
if __name__=="__main__":
    import sys
    app = QApplication(sys.argv)
    w = MyDialog()
    w.resize(600, 400)
    w.show()

    timer = QTimer()
    count = 0
    timer.timeout.connect(w.timer_hook)
    timer.start(1000)
    
    app.exec_()