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
        QGraphicsScene,
        QGraphicsTextItem,
        QPushButton
        )

#import animatedtiles_rc
import math
import random
from axis import Axis
from fortune import Wave
from unitcircle import UnitCircle
from legend import Legend

fortunes = [
"A closed mouth gathers no feet. ",
"A conclusion is simply the place where you got tired of thinking.",
"A cynic is only a frustrated optimist.",
"A foolish man listens to his heart. A wise man listens to the Tau of Fortune.",
"You will die alone and poorly dressed.",
"A fanatic is one who can't change his mind, and won't change the subject.",
"If you look back, you’ll soon be going that way.",
"You will live long enough to hear many things from the Tau of Fortune.",
"An alien of some sort will be appearing to you shortly.",
"Do not mistake temptation for opportunity.",
"Flattery will go far tonight.",
"He who laughs at himself never runs out of things to laugh at.",
"He who laughs last is laughing at you.",
"He who throws dirt is losing ground. ",
"Some men dream of fortunes, others dream of the Tau of Fortune.",
"The greatest danger could be your stupidity. ",
"We don’t know the future, but here’s a cookie.",
"The world may be your oyster, but it doesn't mean you'll get its pearl. ",
"You will be hungry again in one hour.",
"The road to riches is paved with homework.",
"You can always find happiness at work on Friday.",
"Actions speak louder than fortune cookies.",
"Because of your melodic nature, the moonlight never misses an appointment.",
"Don’t behave with cold manners. ",
"Don’t forget you are always on our minds.",
"Fortune not found? Abort, Retry, Ignore.",
"Help! I am being held prisoner in the Tau of Fortune -- stuck in a raspberry pi.",
"Do you really think that there is a Tau of Fortune?",
"Never forget a friend. Especially if he owes you.",
"Never wear your best pants when you go to fight for freedom.",
"Only listen to the Tau of Fortune; disregard all other fortune telling units.",
"It is a good day to have a good day.",
"All fortunes are wrong except this one.",
"Someone will invite you to a Karaoke party.",
"That wasn’t chicken.",
"There is no mistake so great as that of being always right. ",
"You love Chinese food.",
"I am worth a fortune.",
"No snowflake feels responsible in an avalanche.",
"You will receive a fortune cookie.",
"Some fortune cookies contain no fortune.",
"Don’t let statistics do a number on you.",
"You are not illiterate.",
"May you someday be carbon neutral.",
"You have rice in your teeth.",
"Avoid taking unnecessary gambles. Lucky numbers: 12, 15, 23, 28, 37",
"Ask your mom instead of the Tau of Fortune.",
"Hard work pays off in the future. Laziness pays off now.",
"You think it’s a secret, but they know.",
"If a turtle doesn’t have a shell, is it naked or homeless?",
"Change is inevitable, except for vending machines.",
"Don’t eat the raspberry pi."
]
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
            {"wave":Wave('lambda d: sin(d)',QColor(0,0,255))},
            {"wave":Wave('lambda d: cos(d)',QColor(255,128,0))}
        ]
        self.incStep = 15
        cp = QPointF(300,0)
        self.makeWaves(cp)
        self.axis = Axis(QColor(0,0,0))
        self.unitcircle = UnitCircle(Qt.blue,90)
        self.addItem(self.unitcircle)
        self.unitcircle.setPos(QPointF(100,-200))
        self.legend = Legend(self.functions)
        #self.addItem(self.legend)
        self.legend.setPos(QPointF(-200,-350))
        self.addItem(self.axis) 
        self.axis.setPos(self.axis.pos()-cp)
        updateThread.setFunction(self.updateTick)
        button = QPushButton('Fortune')
        button.clicked.connect(self.showFortune)
        widget = self.addWidget(button)
        widget.setPos(QPointF(-200,150))
        self.m_fortunedisplay = QGraphicsTextItem('')
        self.m_raddisplay = QGraphicsTextItem('')
        self.addItem(self.m_fortunedisplay)
        self.addItem(self.m_raddisplay)
        self.m_fortunedisplay.setPos(QPointF(-200,165))
        self.m_raddisplay.setPos(QPointF(100,-150))
        #self.m_fortunedisplay.hide()
        self.m_count = 0
        self.m_numQuestions = 24
    
    def showFortune(self):
        DELTA = .001
        TARGET = 0.0
        currentRad = self.unitcircle.getRad()
        #self.m_fortunedisplay.setHtml('<div style="color:blue;">{0} : {1}</div>'.format(currentRad,abs(currentRad-TARGET)))
        #if abs(self.unitcircle.getRad() - TARGET) < DELTA: # we have a winner
        #    self.m_fortunedisplay.setHtml('<div style="color:blue;font-size:48px;">We Have a Winner!!!</div>')
        #else:
        questionNumber = random.randint(0,len(fortunes)-1)
        self.m_fortunedisplay.setHtml('<div style="color:blue;font-size:20px;">{0}</div>'.format(fortunes[questionNumber]) )
        self.m_fortunedisplay.show()

    def resizeEvent(self, event):
        super(Scene, self).resizeEvent(event)
        self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)

    def updateTick(self,direction):
        self.m_fortunedisplay.hide()
        if direction == 1:
            mult = 1
        else:
            mult = -1
        self.m_count += mult
        [fn["wave"].nextStep(mult*self.incStep) for fn in self.functions]
        self.unitcircle.currentTick = self.functions[0]['wave'].currentTick
        self.m_raddisplay.setHtml('<div style="color:blue;">{0}</div>'.format(self.unitcircle.getRad()))
        #self.unitcircle.nextStep(mult*self.incStep)
        self.update()

    @pyqtSlot(int)
    def speedChange(self,stype):
        newInterval = self.timer.interval() + stype*self.incStep
        if newInterval > 0:
            self.timer.setInterval(newInterval)
