#!/usr/bin/env python3
import math

from PyQt5.QtCore import (pyqtProperty, pyqtSignal, QEasingCurve, QObject,
        QParallelAnimationGroup, QPointF, QPropertyAnimation, qrand, QRectF,
        QState, QStateMachine, Qt, QTimer)
from PyQt5.QtGui import (
    QBrush, 
    QLinearGradient, 
    QPainter, 
    QPainterPath,
    QPixmap,
    QPen
)
from PyQt5.QtWidgets import (QApplication, QGraphicsItem, QGraphicsPixmapItem,
        QGraphicsRectItem, QGraphicsScene, QGraphicsView, QGraphicsWidget,
        QStyle)

class Axis(QGraphicsItem):

    BoundingRect = QRectF(-350,-350,700,700)

    def __init__(self,color):
        super(Axis,self).__init__()
        self.color = color
        self.xres = 2 
        self.yres = 400

    def boundingRect(self):
        return Axis.BoundingRect

    def axes(self):
        qp = QPainterPath() 
        qp.moveTo(QPointF(-350,0))
        qp.lineTo(QPointF(750,0))
        qp.moveTo(QPointF(0,-self.yres))
        qp.lineTo(QPointF(0,self.yres))
        return qp

    def paint(self,painter,option,widget):
        painter.setPen(QPen(Qt.black,0.5))
        painter.drawPath(self.axes())
    