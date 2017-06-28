#!/usr/bin/env python3
from math import pow
import importlib.util
import sys

from PyQt5.QtCore import (
    Qt,
    pyqtSignal
)
from PyQt5.QtGui import (
    QPainter,
    QTransform,
    QIcon
)
from PyQt5.QtWidgets import (
    QAction,
    QMenuBar,
    QMainWindow
)


from view import View

class Window(QMainWindow):
    speedChange = pyqtSignal(int)

    def __init__(self,updateThread):
        super().__init__()
        self.updateThread = updateThread
        self.sineWaveScene()
        self.initUI()


    def initUI(self):

        exitAction = QAction(QIcon(':/assets/images/exit24.png'), 'App Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)


        self.statusBar()

        self.menubar = self.menuBar()
        #print(self.menubar.isNativeMenuBar())
        #self.menubar.setNativeMenuBar(False)
        #print(self.menubar.isNativeMenuBar())
        self.fileMenu = self.menubar.addMenu('&File')
        self.fileMenu.addAction(exitAction)
        self.newMenu = self.menubar.addMenu('&Scene')
        sineWaveAction = QAction(QIcon(':/assets/images/tile.png'), 'Tau Day -- Sine Waves', self)
        sineWaveAction.setShortcut('Ctrl+1')
        sineWaveAction.setStatusTip('Trig Waves')
        sineWaveAction.triggered.connect(self.sineWaveScene)
        self.newMenu.addAction(sineWaveAction)
        roseAction = QAction(QIcon(':/assets/images/tile.png'), 'Tau Day -- Roses', self)
        roseAction.setStatusTip('Roses')
        roseAction.setShortcut('Ctrl+2')
        roseAction.triggered.connect(self.roseScene)
        self.newMenu.addAction(roseAction)
        lissajousAction = QAction(QIcon(':/assets/images/tile.png'), 'Tau Day -- Lissajous Curve', self)
        lissajousAction.setStatusTip('Lissajous')
        lissajousAction.setShortcut('Ctrl+3')
        lissajousAction.triggered.connect(self.lissajousScene)
        self.newMenu.addAction(lissajousAction)
        fortuneAction = QAction(QIcon(':/assets/images/tile.png'), 'Tau Day -- Tau of Fortune', self)
        fortuneAction.setStatusTip('Fortune')
        fortuneAction.setShortcut('Ctrl+4')
        fortuneAction.triggered.connect(self.fortuneScene)
        self.newMenu.addAction(fortuneAction)
        self.setWindowTitle("Sine Waves")
        self.scalefactor = 250

    def scaleView(self):
        scale = pow(2,(self.scalefactor-250)/50.0)
        transform = QTransform()
        transform = transform.scale(scale, scale)
        self.view.setTransform(transform);

    def sineWaveScene(self):
        from wavescene import Scene as WaveScene
        #WScene = importlib.import_module('.wavescene.Scene',package='scenes')
        scene = WaveScene(self.updateThread)
        self.speedChange.connect(scene.speedChange)
        if not hasattr(self,'view'):
            self.view = View(scene,"")
            self.setCentralWidget(self.view)
        self.view.setScene(scene)
        self.setWindowTitle("Sine Waves")

    def fortuneScene(self):
        from fortunescene import Scene as FortuneScene
        scene = FortuneScene(self.updateThread)
        self.speedChange.connect(scene.speedChange)
        self.view.setScene(scene)
        self.setWindowTitle("Tau of Fortune")

    def roseScene(self):
        from rosescene import Scene as RoseScene
        scene = RoseScene(self.updateThread)
        self.speedChange.connect(scene.speedChange)
        self.view.setScene(scene)
        self.setWindowTitle("Rose or Rhodonea Curves")

    def lissajousScene(self):
        from lissajousscene import Scene as LissajousScene
        scene = LissajousScene(self.updateThread)
        self.speedChange.connect(scene.speedChange)
        self.view.setScene(scene)
        #[print('{}'.format(item)) for item in scene.items()]
        self.setWindowTitle("Lissajous Curves")

    def wheelEvent(self,event):
        self.scalefactor += event.angleDelta().y()/60
        self.scaleView()

    def keyPressEvent(self,event):
        super(Window,self).keyPressEvent(event)
        if event.key() == Qt.Key_Plus:
            self.speedChange.emit(-1)
        elif event.key() == Qt.Key_Minus:
            self.speedChange.emit(1)
        elif event.key() == Qt.Key_Less:
            self.scalefactor -= 10
            self.scaleView()
        elif event.key() == Qt.Key_Greater:
            self.scalefactor += 10
            self.scaleView()
