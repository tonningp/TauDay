#!/usr/bin/env python3
import sys
import resources

from PyQt5.QtCore import (
        Qt,
        QTime,
        pyqtSignal,
        qsrand
)
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
        QApplication,
        QMainWindow,
        QPushButton,
        QSplitter,
        QMessageBox,
        QVBoxLayout,
        QHBoxLayout,
        QStyleFactory,
        QWidget,
        QFrame,
        QStyle,
        QAction
)


class App(QMainWindow):
    """
    Resources:
http://www.python-course.eu/index.php
    """
    aboutHTML = """
    Author: Paul Tonning<br>
    License: GPL<br>
    Description: Don't know yet, it's evolving<br>
    Copyright: 2017<br>
    """
    showEditor = pyqtSignal()
    hideEditor = pyqtSignal()
    runCode = pyqtSignal()
    printPDF = pyqtSignal()

    def __init__(self,title):
        super().__init__()
        self.title = title
        self.initUI()
        self.loadEditorView()
        #self.showMaximized()
        self.fullScreen()

    def fullScreen(self):
        self.showFullScreen()

    def help(self):
        QMessageBox.about(self,'About - '+self.title,self.aboutHTML)
    
    def updateStatusBar(self,text):
        self.statusBar().showMessage(text)

    def loadMainView(self):
        from etchlib.scenes.main import Scene as MScene 
        from etchlib.views.mainview import View as MainView
        scene = MScene()
        view = MainView(self)
        self.printPDF.connect(view.onPrintPDF)
        view.setScene(scene)
        vbox = QVBoxLayout()
        vbox.addWidget(view)
        self.setCentralWidget(view)
        scene.initGrid()
        self.runButton.setIconVisibleInMenu(False)
        self.runButton.setVisible(False)

    def loadEditorView(self):
        from etchlib.views.editor import View as EditorView
        from etchlib.widgets.spliteditor import Main as Editor
        editor = Editor()
        self.runCode.connect(editor.onRunCode)
        self.printPDF.connect(editor.onPrintPDF)
        self.setCentralWidget(editor)
        self.runButton.setIconVisibleInMenu(True)
        self.runButton.setVisible(True)
        self.pdfButton.setIconVisibleInMenu(True)
        self.pdfButton.setVisible(True)
    

    def loadMouseMaze(self):
        from etchlib.scenes.maze import Scene as MazeScene 
        from etchlib.views.mouseview import View as MouseView 
        scene = MazeScene()
        self.showEditor.connect(scene.showEditor)
        self.hideEditor.connect(scene.hideEditor)
        view = MouseView(scene,self)
        vbox = QVBoxLayout()
        vbox.addWidget(view)
        self.setCentralWidget(view)
        self.runButton.setIconVisibleInMenu(False)
        self.runButton.setVisible(False)
        self.printPDF.connect(view.onPrintPDF)

    def loadShowEditor(self):
        self.showEditor.emit()

    def loadHideEditor(self):
        self.hideEditor.emit()

    def run_code(self):
        self.runCode.emit()

    def printPDFEmit(self):
        self.printPDF.emit()

    def initUI(self):
        self.setWindowTitle(self.title)
 
        mainMenu = self.menuBar() 
        fileMenu = mainMenu.addMenu('File')
        gameMenu = mainMenu.addMenu('View')
        toolMenu = mainMenu.addMenu('Tools')
        helpMenu = mainMenu.addMenu('Help')
 
        exitButton = QAction(QIcon(':/images/icons/exit64x64.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        self.pdfButton = QAction(QIcon(':/images/icons/pdf64x64.png'), 'PDF', self)
        self.pdfButton.setStatusTip('Print to PDF')
        self.pdfButton.setShortcut('Shift+Ctrl+P')
        self.pdfButton.triggered.connect(self.printPDFEmit)
        fileMenu.addAction(self.pdfButton)
        fileMenu.addAction(exitButton)
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitButton)
        self.toolbar.addAction(self.pdfButton)
        self.runButton = QAction(QIcon(':/images/icons/run64x64.png'), 'Run', self)
        self.runButton.setShortcut('Ctrl+R')
        self.runButton.setStatusTip('Run Code')
        self.runButton.triggered.connect(self.run_code)
        self.toolbar.addAction(self.runButton)

        aboutButton = QAction(QIcon(':/images/icons/about64x64.png'), 'About', self)
        aboutButton.setShortcut('F1')
        aboutButton.setStatusTip('About the application')
        aboutButton.triggered.connect(self.help)
        helpMenu.addAction(aboutButton)
        mouseGameButton = QAction(QIcon(':/images/icons/maze64x64.png'), 'Mouse Maze', self)
        mouseGameButton.setShortcut('Ctrl+G')
        mouseGameButton.setStatusTip('Mouse Maze Game')
        mouseGameButton.triggered.connect(self.loadMouseMaze)
        mainButton = QAction(QIcon(':/images/icons/home64x64.png'), 'Main View', self)
        mainButton.setShortcut('Ctrl+M')
        mainButton.setStatusTip('Main View')
        mainButton.triggered.connect(self.loadMainView)
        editorView = QAction(QIcon(':/images/icons/edit64x64.png'), 'Editor', self)
        editorView.setStatusTip('Editor')
        editorView.setShortcut('Shift+Ctrl+E')
        editorView.triggered.connect(self.loadEditorView)
        gameMenu.addAction(editorView)
        gameMenu.addAction(mouseGameButton)
        gameMenu.addAction(mainButton)
        showEditorButton = QAction(QIcon(':/images/icons/edit64x64.png'), 'Show Editor', self)
        showEditorButton.setShortcut('Ctrl+E')
        showEditorButton.setStatusTip('Show Editor')
        showEditorButton.triggered.connect(self.loadShowEditor)
        toolMenu.addAction(showEditorButton)
        hideEditorButton = QAction(QIcon(':/images/icons/edit64x64.png'), 'Hide Editor', self)
        hideEditorButton.setShortcut('Ctrl+H')
        hideEditorButton.setStatusTip('Hide Editor')
        hideEditorButton.triggered.connect(self.loadHideEditor)
        toolMenu.addAction(hideEditorButton)


        
if __name__ == '__main__':
    now = QTime.currentTime()
    qsrand(now.msec())
    app = QApplication(sys.argv)
    win = App("Lab Tinker")
    sys.exit(app.exec_())
