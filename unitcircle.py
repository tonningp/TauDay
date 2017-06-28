#!/usr/bin/env python3
import math

from PyQt5.QtCore import (
        QPointF, 
        QRectF,
        Qt, 
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

class UnitCircle(QGraphicsItem):

    BoundingRect = QRectF(-50,-50,100,100)

    def __init__(self,color):
        super(UnitCircle,self).__init__()
        self.color = color
        self.xres = 2 
        self.yres = 100
        self.currentTick = 0
        self.m_cp = QPointF(0,0)
        self.m_radius = 50
        self.m_circle = self.getCircle(self.m_radius,self.m_cp,3)

    def getCircle(self,m_radius,cp,ticksize):
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
                QPointF(m_radius*math.cos(math.pi/4)-ticksize,
                        -m_radius*math.sin(math.pi/4)+ticksize),
                QPointF(m_radius*math.cos(math.pi/4)+ticksize,
                        -m_radius*math.sin(math.pi/4)-ticksize)

            ),
            (
                QPointF(0,-m_radius-ticksize),
                QPointF(0,-m_radius+ticksize)
            ),
            # 3pi/4
            (
                QPointF(m_radius*math.cos(3*math.pi/4)-ticksize,
                        -m_radius*math.sin(math.pi/4)-ticksize),
                QPointF(m_radius*math.cos(3*math.pi/4)+ticksize,
                       -m_radius*math.sin(math.pi/4)+ticksize)
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
                QPointF(m_radius*math.cos(5*math.pi/4)-ticksize,
                        -m_radius*math.sin(5*math.pi/4)+ticksize),
                QPointF(m_radius*math.cos(5*math.pi/4)+ticksize,
                       -m_radius*math.sin(5*math.pi/4)-ticksize)
            ),
            # 7pi/4
            (
                QPointF(m_radius*math.cos(7*math.pi/4)-ticksize,
                       -m_radius*math.sin(7*math.pi/4)-ticksize),
                QPointF(m_radius*math.cos(7*math.pi/4)+ticksize,
                       -m_radius*math.sin(7*math.pi/4)+ticksize)
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
        else:
            self.currentTick = 0


    def boundingRect(self):
        return UnitCircle.BoundingRect

    def getRad(self):
        return self.currentTick * math.pi / 180.0 

    def paint(self,painter,option,widget):
        c_size =5 
        rad = self.getRad()
        painter.setPen(QPen(self.color,0.3))
        painter.drawPath(self.m_circle)
        #drawCircle(painter,cp)
        painter.drawLine(self.m_cp,self.m_cp+QPointF(self.m_radius*math.cos(rad),-self.m_radius*math.sin(rad)))
        painter.setBrush(Qt.blue)
        painter.drawEllipse(self.m_cp+QPointF(self.m_radius*math.cos(rad),-self.m_radius*math.sin(rad)),c_size,c_size)
        painter.drawLine(self.m_cp,self.m_cp+QPointF(-self.m_radius*math.cos(rad),self.m_radius*math.sin(rad)))
        painter.setBrush(Qt.red)
        painter.drawEllipse(self.m_cp+QPointF(-self.m_radius*math.cos(rad),self.m_radius*math.sin(rad)),c_size,c_size)
    
