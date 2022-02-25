import sys
import os

from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import (QTabWidget, QMessageBox, QWidget, QLabel,)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont

from Components.MessageBox.CustomizeMessageBox import CustomizeMessageBox_Yes_No
from configuration import Configuration
from codeeditor import CodeEditor
from widgets import MessageBox
# from Components.StartPage.startpage import StartPage

import widgets
class TabWidget(QTabWidget):
    tabClosingSignal = pyqtSignal(name='closingTab')
    def __init__(self, parent=None):
        super().__init__()
        
        self.mainWindow = parent
        self.mainWindow.setObjectName("tabWidgetMainWindow")
        self.tabBar().setObjectName("tabWidgetTabBar")

        self.c = Configuration()
        self.font = QFont()
        self.font.setFamily(self.c.getEditorFont())
        self.font.setPointSize(self.c.getEditorFontSize())

        self.tabBar().setFont(self.font)
        self.setMovable(True)
        self.setTabsClosable(True)

        # signals
        self.tabCloseRequested.connect(self.closeTab)
        self.currentChanged.connect(self.changeTab)
        self.textPad = None
        self.codeView = None

        # self.starterPage = None

    def newTab(self, editor=None, codeView=None):

        if editor:
            if editor.filename == None:
                self.addTab(editor, "Program*")
            else:
                self.addTab(editor, os.path.basename(editor.filename))
                x = self.count() - 1
                self.setTabToolTip(x, editor.filename)
                self.codeView = self.mainWindow.codeView



    def closeTab(self, index):
        self.tabClosingSignal.emit()
        x = self.currentIndex()
        if x != index:
            self.setCurrentIndex(index)
        
        tabText = self.tabText(index)
        
        if '*' in tabText:
            self.index = index
            CustomizeMessageBox_Yes_No('Dosya Kaydedilmedi<br><br>Şimdi Kaydet ?', clickAccept=self.saveYesClick, clickCancel=self.saveNoClick)
        else:
            self.removeTab(index)
        
        x = self.currentIndex()
        self.setCurrentIndex(x)
        
        if x == -1:
            self.refreshCodeView('')
            self.mainWindow.setWindowTitle('PyNar Kod Editörü')
            self.mainWindow.changeToolbarButtonActive(False)

    def saveYesClick(self):
        self.mainWindow.save()
        self.removeTab(self.index)

    def saveNoClick(self):
        self.removeTab(self.index)
    
    def changeTab(self, index):
        x = self.count()
        y = x - 1
        
        if y >= 0:
            self.setCurrentIndex(index)
            textPad = self.currentWidget()
            self.textPad = textPad
            text = self.textPad.text()
            
            if self.codeView:
                self.refreshCodeView(text)
            else:
                self.codeView = self.mainWindow.codeView
                self.refreshCodeView(text)
                # self.setStyleSheet(
                #     '''
                #     background-color: white;
                #
                #     ''')
        # else:
        #     self.mainWindow.refresh(self.starterPage)
            # self.setStyleSheet(
            #     '''
            #     QTabBarbackground-color: rgb(197, 255, 255);
            #
            #     ''')
        
        if self.textPad:
            self.mainWindow.refresh(self.textPad)
   
    def refreshCodeView(self, text=None):
       if text:
            text = text
            codeViewDict = self.codeView.makeDictForCodeView(text)
            self.codeView.updateCodeView(codeViewDict)
    
    def getCurrentTextPad(self):
        textPad = self.currentWidget()
        return textPad
  