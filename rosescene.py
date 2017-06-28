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
        QGraphicsScene,QGraphicsItem
        )

#import animatedtiles_rc
from axis import Axis
from rose import Curve
from unitcircle import UnitCircle
from legend import Legend

class Scene(QGraphicsScene):


    def addWave(self,wave):
        self.addItem(wave)

    def makeWaves(self,cp):
        [self.addItem(fn['wave']) for fn in self.functions]

        #for fn in self.functions:
        #    curve = fn['wave']
        #    self.addItem(curve)
        #    curve.setPos(fn['pos'])

    def __init__(self,updateThread):
        super(Scene,self).__init__(-350, -350, 900, 700)
        self.functions = [
                {"wave":Curve('(cos(2*d)*cos(d),cos(2*d)*sin(d))',QColor(0,255,255),4),'pos':QPointF(-200,-300)},
                {"wave":Curve('(cos(3/2.0*d)*cos(d),cos(3/2.0*d)*sin(d))',QColor(128,0,255),2),'pos':QPointF(-100,-300)},
                {"wave":Curve('(cos(7/8.0*d)*cos(d),cos(7/8.0*d)*sin(d))',QColor(0,0,255),8),'pos':QPointF(0,-300)},
                {"wave":Curve('(cos(3/4.0*d)*cos(d),cos(3/4.0*d)*sin(d))',QColor(255,0,0),4),'pos':QPointF(100,-300)},
                    {"wave":Curve('(cos(3/8.0*d)*cos(d),cos(3/8.0*d)*sin(d))',QColor(0,255,0),8),'pos':QPointF(200,-300)},
                    {"wave":Curve('(cos(1/3.0*d)*cos(d),cos(1/3.0*d)*sin(d))',QColor(0,0,255),2),'pos' : QPointF(-200,-200)},
        ]
        self.incStep = 5 
        cp = QPointF(300,0)
        self.makeWaves(cp)
        self.axis = Axis(QColor(0,0,0))
        self.unitcircle = UnitCircle(Qt.blue)
        self.unitcircle.setFlag(QGraphicsItem.ItemIsMovable, True);
        self.unitcircle.setFlag(QGraphicsItem.ItemIsSelectable, True);
        self.unitcircle.setPos(QPointF(-250,-275))
        self.legend = Legend(self.functions)
        self.addItem(self.unitcircle)
        updateThread.setFunction(self.updateTick)
        #self.timer = QTimer()
        #self.timer.timeout.connect(self.updateTick)
        #self.timer.start(50)

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
