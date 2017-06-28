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
from wave import Wave
from unitcircle import UnitCircle
from legend import Legend

class Scene(QGraphicsScene):


    def addWave(self,wave,cp):
        self.addItem(wave)
        #wave.setPos(wave.pos()-cp)
        wave.setPos(QPointF(-300,0))

    def makeWaves(self,cp):
        [self.addWave(fn['wave'],cp) for fn in self.functions]

    def __init__(self,updateThread):
        super(Scene,self).__init__(-350, -350, 900, 700)
        self.functions = [
            {"wave":Wave('lambda d: cos(2*pi*(3*d))*exp(-pi*d*d)',QColor(0,0,255))},
            {"wave":Wave('lambda d: sin(d)',QColor(0,0,255))},
            {"wave":Wave('lambda d: cos(d)',QColor(255,128,0))},
            {"wave":Wave('lambda d: sin(4*d)*-2.5',QColor(0,128,128))},
            {"wave":Wave('lambda d: cos(4*d)*0.5',QColor(0,128,128))},
        ]
        self.incStep = 15
        cp = QPointF(300,0)
        self.makeWaves(cp)
        self.axis = Axis(QColor(0,0,0))
        self.unitcircle = UnitCircle(Qt.blue)
        self.addItem(self.unitcircle)
        self.unitcircle.setPos(QPointF(-300,-275))
        self.legend = Legend(self.functions)
        self.addItem(self.legend)
        self.legend.setPos(QPointF(-200,-350))
        self.addItem(self.axis) 
        self.axis.setPos(self.axis.pos()-cp)
        updateThread.setFunction(self.updateTick)
        #self.timer = QTimer()
        #self.timer.timeout.connect(self.updateTick)
        #self.timer.start(100)

    def resizeEvent(self, event):
        super(Scene, self).resizeEvent(event)
        self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)

    def updateTick(self,direction):
        if direction == 1:
            mult = 1
        else:
            mult = -1
        [fn["wave"].nextStep(mult*self.incStep) for fn in self.functions]
        self.unitcircle.nextStep(mult*self.incStep)
        self.update()

    @pyqtSlot(int)
    def speedChange(self,stype):
        newInterval = self.timer.interval() + stype*self.incStep
        if newInterval > 0:
            self.timer.setInterval(newInterval)
