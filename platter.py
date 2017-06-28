#!/usr/bin/env python3
import pigpio
import threading
import time
import math
from PyQt5.QtCore import (
    Qt,
    QObject,
    QRunnable,
    QThread,
    QCoreApplication,
    pyqtSignal
)



ENCODE_PIN = 18
DIR_PIN = 23
COUNTS_PER_REV = 24
RADIANS_PER_CLICK = (math.pi * 2) / COUNTS_PER_REV

class RadianEmitter(QObject):
    sig = pyqtSignal(int)
    def __init__(self,parent=0):
        super().__init__()
    
    def setFunction(self,f):
        self.sig.connect(f)

    def send(self,f):
        self.sig.emit(f)

        
class TauReader(QThread):
    count = 0
    current_rad = 0;

    def setEmitter(self,emitter):
        self.emitter = emitter

    def setFunction(self,f):
        self.emitter.setFunction(f)

    def run(self):
        pi = pigpio.pi()
        pi.set_mode(ENCODE_PIN, pigpio.INPUT)
        pi.set_pull_up_down(ENCODE_PIN, pigpio.PUD_DOWN)
        pi.set_mode(DIR_PIN, pigpio.INPUT)
        pi.set_pull_up_down(DIR_PIN, pigpio.PUD_DOWN)
        while True:  # include the main thread
            start_time = time.time()
            if pi.wait_for_edge(ENCODE_PIN,pigpio.EITHER_EDGE):
                direction = pi.read(DIR_PIN)
                if direction == 1:
                    TauReader.count += 1
                    TauReader.current_rad += RADIANS_PER_CLICK
                else:
                    TauReader.count -= 1
                    TauReader.current_rad -= RADIANS_PER_CLICK
                if self.count > COUNTS_PER_REV:
                    TauReader.count = 0
                    TauReader.current_rad = 0
                if self.count < 0:
                    TauReader.count = COUNTS_PER_REV 
                    TauReader.current_rad = 2 * math.pi
                if direction == 1:
                    direction = 0
                else:
                    direction = 1;
                self.emitter.send(direction)
#              print("Tick: {0} Radians: {1}"
#                      .format(TauReader.count,TauReader.current_rad))
            else:
                print("wait for edge timed out")

def receiver(value):
    print("direction: {0}".format(value))

if __name__ == '__main__':
        import sys
        app = QCoreApplication([])
        treader = TauReader()  # ...Instantiate a thread and pass a unique ID to it
        treader.finished.connect(app.exit)
        re = RadianEmitter()
        treader.setEmitter(re)
        treader.setFunction(receiver);
        treader.start()                                   # ...Start the thread
        print("Reading")
        sys.exit(app.exec_())

