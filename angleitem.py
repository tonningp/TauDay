#!/usr/bin/env python3
from math import sin,cos,pi

from PyQt5.QtCore import (
        QPointF, 
        QRectF,
        Qt, 
)

from PyQt5.QtGui import (
    QBrush, 
    QPen,
    QFont,
    QColor,
    QPainter, 
    QPainterPath,
    QPixmap
)
from PyQt5.QtWidgets import (
    QGraphicsItem
)

class Item(QGraphicsItem):

    BoundingRect = QRectF(-50,-50,100,100)

    def __init__(self,parent=0):
        super(Item,self).__init__(parent)
        self.xres = 2 
        self.yres = 100
        self.m_ballsize = 2.5
        self.m_radius = 10
        self.currentTick = 0
        self.m_cp = QPointF(0,0)
#        self.m_circle = self.getCircle(self.m_radius,self.m_cp,3)

    def getCircle(self,radius,cp,ticksize):
        qp = QPainterPath()
        qp.addEllipse(cp,self.m_radius,self.m_radius)
        points = [

            # 0
            (
                QPointF(self.m_radius-ticksize,0),
                QPointF(self.m_radius+ticksize,0)
            ),
            #pi/4
            (
                QPointF(self.m_radius*cos(pi/4)-ticksize,
                        -self.m_radius*sin(pi/4)+ticksize),
                QPointF(self.m_radius*cos(pi/4)+ticksize,
                        -self.m_radius*sin(pi/4)-ticksize)

            ),
            (
                QPointF(0,-self.m_radius-ticksize),
                QPointF(0,-self.m_radius+ticksize)
            ),
            # 3pi/4
            (
                QPointF(self.m_radius*cos(3*pi/4)-ticksize,
                        -self.m_radius*sin(pi/4)-ticksize),
                QPointF(self.m_radius*cos(3*pi/4)+ticksize,
                       -self.m_radius*sin(pi/4)+ticksize)
            ),
            # 180
            (
                QPointF(-self.m_radius-ticksize,0),
                QPointF(-self.m_radius+ticksize,0)

            ),
            # 3pi/2
            (
                QPointF(0,self.m_radius-ticksize),
                QPointF(0,self.m_radius+ticksize)
            ),
            (
                QPointF(self.m_radius*cos(5*pi/4)-ticksize,
                        -self.m_radius*sin(5*pi/4)+ticksize),
                QPointF(self.m_radius*cos(5*pi/4)+ticksize,
                       -self.m_radius*sin(5*pi/4)-ticksize)
            ),
            # 7pi/4
            (
                QPointF(self.m_radius*cos(7*pi/4)-ticksize,
                       -self.m_radius*sin(7*pi/4)-ticksize),
                QPointF(self.m_radius*cos(7*pi/4)+ticksize,
                       -self.m_radius*sin(7*pi/4)+ticksize)
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
        return Item.BoundingRect

    def getRad(self):
        return self.currentTick * pi / 180.0 

    def setCenter(self,cp):
        self.m_cp = cp 

    def paint(self,painter,option,widget):
        painter.setPen(QPen(Qt.blue,0.25)) 
        rad = self.getRad()
        painter.drawLine(self.m_cp,self.m_cp+QPointF(self.m_radius*cos(rad),-self.m_radius*sin(rad)))
        painter.drawLine(self.m_cp,self.m_cp+QPointF(self.m_radius/2*cos(rad+pi/2),-self.m_radius/2*sin(rad+pi/2)))
        painter.drawLine(self.m_cp,self.m_cp+QPointF(-self.m_radius*cos(rad),self.m_radius*sin(rad)))
        painter.drawLine(self.m_cp,self.m_cp+QPointF(-self.m_radius/2*cos(rad+pi/2),self.m_radius/2*sin(rad+pi/2)))
        painter.setBrush(Qt.blue)
        painter.drawEllipse(self.m_cp+QPointF(self.m_radius*cos(rad),-self.m_radius*sin(rad)),self.m_ballsize,self.m_ballsize)
        painter.setBrush(Qt.red)
        painter.drawEllipse(self.m_cp+QPointF(-self.m_radius*cos(rad),self.m_radius*sin(rad)),self.m_ballsize,self.m_ballsize)
        painter.setBrush(Qt.black)
        painter.drawEllipse(self.m_cp+QPointF(self.m_radius/2*cos(rad+pi/2),-self.m_radius/2*sin(rad+pi/2)),
                            self.m_ballsize/1.5,self.m_ballsize/1.5)
        #
        #painter.setBrush(QColor(255,0,255))
        painter.drawLine(
                           self.m_cp+QPointF(-self.m_radius/2*cos(rad+pi/2)-10,self.m_radius/2*sin(rad+pi/2)),
                           self.m_cp+QPointF(-self.m_radius/2*cos(rad+pi/2)+10,self.m_radius/2*sin(rad+pi/2))

                        )
        font = QFont() 
        font.setPointSize(5)
        painter.setFont(font)
        painter.drawText(
                           self.m_cp+QPointF(-self.m_radius/2*cos(rad+pi/2)-10,self.m_radius/2*sin(rad+pi/2)),
                           str(self.currentTick)
                        )
