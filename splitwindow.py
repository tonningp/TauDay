#!/usr/bin/env python3
import sys
import resources_qrc

from PyQt5.QtCore import (
        Qt,
        QTime,
        pyqtSignal,
        qsrand
)
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
        QApplication,
        QMainWindow,
        QPushButton,
        QSplitter,
        QMessageBox,
        QVBoxLayout,
        QHBoxLayout,
        QStyleFactory,
        QWidget,
        QFrame,
        QStyle,
        QAction
)


class App(QMainWindow):
    """
    Resources:
http://www.python-course.eu/index.php
    """
    aboutHTML = """
    Author: Paul Tonning<br>
    License: GPL<br>
    Description: Don't know yet, it's evolving<br>
    Copyright: 2017<br>
    """
    showEditor = pyqtSignal()
    hideEditor = pyqtSignal()
    runCode = pyqtSignal()
    printPDF = pyqtSignal()

    def __init__(self,title):
        super().__init__()
        self.title = title
        self.initUI()
        #self.showMaximized()
        self.fullScreen()

    def fullScreen(self):
        self.showFullScreen()

    def help(self):
        QMessageBox.about(self,'About - '+self.title,self.aboutHTML)
    
    def updateStatusBar(self,text):
        self.statusBar().showMessage(text)

    def sineWaveScene(self):
        from wavescene import Scene as WaveScene
        scene = WaveScene()
        self.view.setScene(scene)
        self.setWindowTitle("Sine Waves")

    def roseScene(self):
        from rosescene import Scene as RoseScene
        scene = RoseScene()
        self.view.setScene(scene)
        self.setWindowTitle("Rose or Rhodonea Curves")

    def lissajousScene(self):
        from lissajousscene import Scene as LissajousScene
        scene = LissajousScene()
        self.view.setScene(scene)
        self.setWindowTitle("Lissajous Curves")

    def initUI(self):
        self.setWindowTitle(self.title)
 
        mainMenu = self.menuBar() 
        fileMenu = mainMenu.addMenu('File')
        gameMenu = mainMenu.addMenu('View')
        toolMenu = mainMenu.addMenu('Tools')
        helpMenu = mainMenu.addMenu('Help')
 
        exitButton = QAction(QIcon(':/assets/images/exit64x64.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        self.pdfButton = QAction(QIcon(':/assets/images/pdf64x64.png'), 'PDF', self)
        self.pdfButton.setStatusTip('Print to PDF')
        self.pdfButton.setShortcut('Shift+Ctrl+P')
        self.pdfButton.triggered.connect(lambda: self.printPDF.emit())
        fileMenu.addAction(self.pdfButton)
        fileMenu.addAction(exitButton)
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitButton)
        self.toolbar.addAction(self.pdfButton)
        self.runButton = QAction(QIcon(':/assets/images/run64x64.png'), 'Run', self)
        self.runButton.setShortcut('Ctrl+R')
        self.runButton.setStatusTip('Run Code')
        self.runButton.triggered.connect(lambda: self.runCode.emit())
        self.toolbar.addAction(self.runButton)
        aboutButton = QAction(QIcon(':/assets/images/about64x64.png'), 'About', self)
        aboutButton.setShortcut('F1')
        aboutButton.setStatusTip('About the application')
        aboutButton.triggered.connect(self.help)
        helpMenu.addAction(aboutButton)


        
if __name__ == '__main__':
    now = QTime.currentTime()
    qsrand(now.msec())
    app = QApplication(sys.argv)
    win = App("Lab Tinker")
    sys.exit(app.exec_())
