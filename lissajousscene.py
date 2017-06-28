#!/usr/bin/env python3
from PyQt5.QtCore import (
        QPointF, 
        Qt,
        pyqtSlot,
        QTimer)
from PyQt5.QtGui import (
    QColor
    )
from PyQt5.QtWidgets import (
        QGraphicsScene
        )

#import animatedtiles_rc
from axis import Axis
from lissajous import Curve
from unitcircle import UnitCircle
from legend import Legend

class Scene(QGraphicsScene):


    def addWave(self,wave,cp):
        self.addItem(wave)
        #wave.setPos(wave.pos()-cp)
        #wave.setPos(QPointF(-300,0))

    def makeWaves(self,cp):
        [self.addWave(fn['wave'],cp) for fn in self.functions]

    def __init__(self,updateThread):
        super(Scene,self).__init__(-350, -350, 900, 700)
        self.functions = [
            {"wave":Curve('(sin(3*t+pi/2),sin(4*t))',QColor(255,0,0),1)},
            {"wave":Curve('(sin(5*t+pi/2),sin(6*t))',QColor(0,255,0),1)},
            {"wave":Curve('(sin(7*t+pi/2),sin(8*t))',QColor(0,0,255),1)},
            {"wave":Curve('(sin(11*t+pi/2),sin(12*t))',QColor(255,0,0),1)},
            {"wave":Curve('(sin(13*t+pi/2),sin(14*t))',QColor(0,255,0),1)},
            {"wave":Curve('(sin(15*t+pi/2),sin(16*t))',QColor(0,0,255),1)},
        ]
        self.incStep = 15
        cp = QPointF(300,0)
        self.makeWaves(cp)
        self.axis = Axis(QColor(0,0,0))
        self.unitcircle = UnitCircle(Qt.blue)
        self.addItem(self.unitcircle)
        self.unitcircle.setPos(QPointF(-300,-275))
        updateThread.setFunction(self.updateTick)
        #self.timer = QTimer()
        #self.timer.timeout.connect(self.updateTick)
        #self.timer.start(33)

    def resizeEvent(self, event):
        super(Scene, self).resizeEvent(event)
        self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)

    def updateTick(self,direction):
        if direction == 1:
            mult = 1
        else:
            mult = -1
        [fn["wave"].nextStep(mult*self.incStep) for fn in self.functions]
        self.unitcircle.nextStep(self.incStep)
        self.update()

    @pyqtSlot(int)
    def speedChange(self,stype):
        newInterval = self.timer.interval() + stype*self.incStep
        if newInterval > 0:
            self.timer.setInterval(newInterval)
