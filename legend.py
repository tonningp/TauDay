#!/usr/bin/env python3
import math

from PyQt5.QtCore import (
        QPointF, 
        QRectF,
        Qt, 
)

from PyQt5.QtGui import (
    QBrush, 
    QPainter, 
    QPainterPath,
    QFont,
    QPixmap
)
from PyQt5.QtWidgets import (
    QGraphicsItem, 
    QGraphicsScene
)

class LegendItem(QPainterPath):

    def __init__(self,rect,item):
        super(LegendItem,self).__init__()
        #self.addRect(rect)
        self.m_item = item 
        font = QFont()
        font.setBold(True)
        self.addText(rect.x(),rect.top()+10,font,item['wave'].fnText)

    def getItem(self):
        return self.m_item

class Legend(QGraphicsItem):

    BoundingRect = QRectF(0,0,250,75)

    def __init__(self,plots):
        super(Legend,self).__init__()
        self.m_plots = plots
        self.m_items = []
        rect = QRectF(5,5,25,25)
        for r in self.m_plots:
            self.m_items.append(LegendItem(rect,r))
            rect.setY(rect.y() + 15)

    def boundingRect(self):
        return Legend.BoundingRect

    def mousePressEvent(self,event):
        pass
       # print(event.pos())

    def paint(self,painter,option,widget):
        #painter.setBrush(Qt.blue)
        #painter.drawRect(self.boundingRect());
        for item in self.m_items:
            painter.setPen(item.getItem()['wave'].color)
            painter.setBrush(item.getItem()['wave'].color)
            painter.drawPath(item)
    
