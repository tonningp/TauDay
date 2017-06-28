#!/usr/bin/env python3

from PyQt5.QtWidgets import (
    QApplication
)
from PyQt5.QtGui import (
        QIcon
)
import resources_qrc
from mainwindow import Window as MainWindow
import platter

if __name__ == '__main__':

    import sys
    import math

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('pi-symbol.png'))
    treader = platter.TauReader()  
    treader.finished.connect(app.exit)
    re = platter.RadianEmitter()
    treader.setEmitter(re)
#    treader.setFunction(receiver);
    treader.start()                                   # ...Start the thread
    window = MainWindow(treader)
    window.show()
    sys.exit(app.exec_())
