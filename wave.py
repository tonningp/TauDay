#!/usr/bin/env python3
from math import sin,cos,pi,exp

from PyQt5.QtCore import (
        QPointF, 
        QRectF,
        Qt, 
        QTimer
)
from PyQt5.QtGui import (
    QBrush, 
    QPen,
    QPainter, 
    QPainterPath,
    QPixmap
)
from PyQt5.QtWidgets import (
    QGraphicsItem, 
    QGraphicsScene
)

from angleitem import Item as Angle
class Wave(QGraphicsItem):

    BoundingRect = QRectF(0,-100,720,100)

    def __init__(self,fn,color):
        super(Wave,self).__init__()
        self.fnText = fn
        self.fn = eval(fn)
        self.color = color
        self.xres = 2 
        self.yres = 100
        self.start = 0
        self.currentTick = self.start
        self.curve = self.getCurve()
        self.setFlag(QGraphicsItem.ItemIsMovable, True);
        self.setFlag(QGraphicsItem.ItemIsSelectable, True);
        self.angle = Angle(self)

    def getCurve(self):
       qp = QPainterPath()
       lastPoint = QPointF(0,-1*self.yres * self.fn(self.start))
       for d in range(self.start,360):
           qp.moveTo(lastPoint)
           nextPoint = QPointF(self.xres * d,-1*self.yres * self.fn(d*pi/180.0))
           qp.lineTo(nextPoint)
           lastPoint = nextPoint

       return qp 



    def boundingRect(self):
        return Wave.BoundingRect

    def getRad(self):
        return self.currentTick * pi / 180.0 

    def unitCircle(self,m_radius,cp,ticksize):
        qp = QPainterPath()
        qp.addEllipse(cp,m_radius,m_radius)
        points = [

            # 0
            (
                QPointF(m_radius-ticksize,0),
                QPointF(m_radius+ticksize,0)
            ),
            #pi/4
            (
                QPointF(m_radius*cos(pi/4)-ticksize,
                        -m_radius*sin(pi/4)+ticksize),
                QPointF(m_radius*cos(pi/4)+ticksize,
                        -m_radius*sin(pi/4)-ticksize)

            ),
            (
                QPointF(0,-m_radius-ticksize),
                QPointF(0,-m_radius+ticksize)
            ),
            # 3pi/4
            (
                QPointF(m_radius*cos(3*pi/4)-ticksize,
                        -m_radius*sin(pi/4)-ticksize),
                QPointF(m_radius*cos(3*pi/4)+ticksize,
                       -m_radius*sin(pi/4)+ticksize)
            ),
            # 180
            (
                QPointF(-m_radius-ticksize,0),
                QPointF(-m_radius+ticksize,0)

            ),
            # 3pi/2
            (
                QPointF(0,m_radius-ticksize),
                QPointF(0,m_radius+ticksize)
            ),
            (
                QPointF(m_radius*cos(5*pi/4)-ticksize,
                        -m_radius*sin(5*pi/4)+ticksize),
                QPointF(m_radius*cos(5*pi/4)+ticksize,
                       -m_radius*sin(5*pi/4)-ticksize)
            ),
            # 7pi/4
            (
                QPointF(m_radius*cos(7*pi/4)-ticksize,
                       -m_radius*sin(7*pi/4)-ticksize),
                QPointF(m_radius*cos(7*pi/4)+ticksize,
                       -m_radius*sin(7*pi/4)+ticksize)
            )
        ]

       # build the tick marks
        for pair in points:
            qp.moveTo(cp+pair[0])
            qp.lineTo(cp+pair[1])

        qp.addEllipse(cp,2,2)

        return qp

    def nextStep(self,inc):
        if self.currentTick  < 360: 
            self.currentTick +=inc
            if self.currentTick < 0:
                self.currentTick = 359
        else:
            self.currentTick = 0

        #else:
        #    self.currentTick = self.start
        #if self.currentTick < 0:
        #    self.currentTick = 359
        self.angle.currentTick = self.currentTick

    def paint(self,painter,option,widget):
        painter.setPen(QPen(self.color,2.25))
        painter.drawPath(self.curve)
        self.angle.setCenter(QPointF( self.xres*self.currentTick,
                                     -self.yres*self.fn(self.getRad())))
