import sys, stat
import os
from PyQt5 import Qt
from PyQt5.QtCore import QSize, QRect, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QWidget, QDialog, QHBoxLayout,
                             QVBoxLayout, QGridLayout, QLabel, QLineEdit,
                             QPushButton, QMainWindow, QCheckBox, QDesktopWidget,
                             QGroupBox, QSpinBox, QTextEdit, QTabWidget,
                             QDialogButtonBox, QMessageBox, QListWidget,
                             QListWidgetItem, QComboBox, QFontDialog)
from PyQt5.QtGui import (QFont, QPalette, QIcon)
from Components.MessageBox.CustomizeMessageBox import CustomizeMessageBox_Yes_No, CustomizeMessageBox_Ok
from PyQt5.Qt import Qt
from configuration import Configuration
from widgets import (MessageBox, Label, RadioButton, PushButton,
                     ListWidget, WhiteLabel, TabWidget, TextEdit)
from deadcodechecker import DeadCodeChecker
from pycodechecker import PyCodeChecker
from natsort import natsorted
import urllib
from urllib import parse
import requests
import subprocess,json
from threading import Thread
import re
import configparser
from dialog import Dialog,fontDialog

class SettingsDialog(Dialog):
    def __init__(self, parent=None, textPad=None):
        super().__init__(parent, textPad)
        self.parent = parent
        self.textPad = textPad
        self.c = Configuration()
        self.setWindowTitle('Editör Ayarları')
        self.setWindowIcon(QIcon(':/icon/images/settings_i.png'))
        self.setStyleSheet("background-color: #CAD7E0;")
        self.setMinimumSize(QSize(600, 363))
        self.setMaximumSize(QSize(600, 363))
        self.initUI()

    def initUI(self):
        font = QFont()
        font.setFamily(self.c.getEditorFont())
        font.setPointSize(self.c.getEditorFontSize())

        self.codeFontDialog = QFontDialog()

        self.editorFontDialog = QFontDialog()

        groupBox = QWidget()
        groupBox.setFont(font)
        groupBox.setGeometry(QRect(0, 0, 500, 300))
        groupBox.setStyleSheet(" background-color: rgb(255, 255, 255);")
        groupBox.setObjectName("settingsTab")

        labelEditor = Label(groupBox)
        labelEditor.setGeometry(QRect(30, 38, 255, 25))
        labelEditor.setText('Editör Yazı Tipi ve Boyutu:')
        labelEditor.setFont(font)
        labelEditor.setObjectName("settingsMenu")

        self.editorBox = QLineEdit(groupBox)
        self.editorBox.setGeometry(QRect(295, 40, 150, 25))
        self.editorBox.setReadOnly(True)
        self.editorBox.setText(self.c.getEditorFont())
        self.editorBox.setFont(font)

        self.editorSizeBox = QLineEdit(groupBox)
        self.editorSizeBox.setGeometry(QRect(455, 40, 30, 25))
        self.editorSizeBox.setReadOnly(True)
        self.editorSizeBox.setText(str(self.c.getEditorFontSize()))
        self.editorSizeBox.setFont(font)


        labelChangeEditor = clickableLabel(groupBox)
        labelChangeEditor.setGeometry(QRect(495, 40, 100, 22))
        labelChangeEditor.setText("[" + "<a href=#>Değiştir</a>" + "]")
        labelChangeEditor.setFont(font)
        labelChangeEditor.clicked.connect(self.changeEditorFont)
        labelChangeEditor.setObjectName("settingsMenu")

        labelCode = Label(groupBox)
        labelCode.setGeometry(QRect(30, 68, 255, 25))
        labelCode.setText('Kod Yazı Tipi ve Boyutu:')
        labelCode.setFont(font)
        labelCode.setObjectName("settingsMenu")

        self.codeBox = QLineEdit(groupBox)
        self.codeBox.setGeometry(QRect(295, 70, 150, 25))
        self.codeBox.setReadOnly(True)
        self.codeBox.setText(self.c.getCodeFont())
        self.codeBox.setFont(font)

        self.codeSizeBox = QLineEdit(groupBox)
        self.codeSizeBox.setGeometry(QRect(455, 70, 30, 25))
        self.codeSizeBox.setReadOnly(True)
        self.codeSizeBox.setText(str(self.c.getFontSize()))
        self.codeSizeBox.setFont(font)

        labelChangeCode = clickableLabel(groupBox)
        labelChangeCode.setGeometry(QRect(495, 70, 100, 22))
        labelChangeCode.setText("[" + "<a href=#>Değiştir</a>" + "]")
        labelChangeCode.setFont(font)
        labelChangeCode.clicked.connect(self.changeCodeFont)
        labelChangeCode.setObjectName("settingsMenu")

        label1 = Label(groupBox)
        label1.setGeometry(QRect(30, 98, 320, 25))
        label1.setText('<Tab> Tuşu Genişliği:')
        label1.setFont(font)
        label1.setObjectName("settingsMenu")


        self.tabWidthBox = QSpinBox(groupBox)
        self.tabWidthBox.setMinimum(2)
        self.tabWidthBox.setMaximum(10)
        self.tabWidthBox.setGeometry(QRect(295, 101, 42, 22))
        self.tabWidthBox.setFont(font)
        tab = int(self.c.getTab())
        self.tabWidthBox.setValue(tab)
        self.tabWidthBox.setObjectName("settingsSpinBox")


        labelChatbot = WhiteLabel(groupBox)
        labelChatbot.setGeometry(QRect(30, 131, 250, 22))
        labelChatbot.setText('Hata düzeltme için sohbet robotunu kullan:')
        labelChatbot.setFont(font)
        labelChatbot.setObjectName("settingsMenu")

        self.chatbotStatus = QCheckBox(groupBox)
        self.chatbotStatus.setGeometry(QRect(295, 134, 20, 20))
        self.chatbotStatus.setStyleSheet("color:rgb(82, 95, 99)")
        self.chatbotStatus.setFont(font)
        self.chatbotStatus.setCheckState(0 if self.c.getParam('ChatbotStatus', 'ChatbotStatus') == "False" else 1)
        self.chatbotStatus.setTristate(0)
        self.chatbotStatus.setObjectName("settingsCheckBox")


        labelLogging = WhiteLabel(groupBox)
        labelLogging.setGeometry(QRect(30, 161, 195, 22))
        labelLogging.setText('Kullanım Verilerini Kaydet:')
        labelLogging.setFont(font)
        labelLogging.setObjectName("settingsMenu")

        self.loggingCase = QCheckBox(groupBox)
        self.loggingCase.setGeometry(QRect(295, 164, 20, 20))
        self.loggingCase.setStyleSheet("color:rgb(82, 95, 99)")
        self.loggingCase.setFont(font)
        self.loggingCase.setCheckState(0 if self.c.getParam('Logging', 'logging') == "False" else 1)
        self.loggingCase.setTristate(0)
        self.loggingCase.setObjectName("settingsCheckBox")


        self.checkExam = QCheckBox(groupBox)
        self.checkExam.setGeometry(QRect(295, 194, 20, 20))
        self.checkExam.setStyleSheet("color:rgb(82, 95, 99)")
        self.checkExam.setFont(font)
        self.checkExam.setCheckState(0 if self.c.getParam('ExamLogging', 'ExamLogging') == "False" else 1)
        self.checkExam.setTristate(0)
        self.checkExam.setObjectName("settingsCheckBox")


        labelExamDataPermit = WhiteLabel(groupBox)
        labelExamDataPermit.setGeometry(QRect(30, 191, 195, 22))
        labelExamDataPermit.setText('Sınav Verilerini Kaydet:')
        labelExamDataPermit.setFont(font)
        labelExamDataPermit.setObjectName("settingsMenu")

        labelYes = WhiteLabel(groupBox)
        labelYes.setGeometry(QRect(317, 162, 70, 22))
        labelYes.setText('Evet')
        labelYes.setFont(font)
        labelYes.setObjectName("settingsMenu")

        labelChatbotYes = WhiteLabel(groupBox)
        labelChatbotYes.setGeometry(QRect(317, 132, 70, 22))
        labelChatbotYes.setText('Evet')
        labelChatbotYes.setFont(font)
        labelChatbotYes.setObjectName("settingsMenu")

        labelExamYes = WhiteLabel(groupBox)
        labelExamYes.setGeometry(QRect(317, 192, 300, 22))
        labelExamYes.setText('Evet(Sınav olabilmeniz için zorunludur.)')
        labelExamYes.setFont(font)
        labelExamYes.setObjectName("settingsMenu")

        labelData = WhiteLabel(groupBox)
        labelData.setGeometry(QRect(30, 221, 200, 22))
        labelData.setText("Kullanım Verileri:")
        labelData.setFont(font)
        labelData.setObjectName("settingsMenu")

        labelDelete = clickableLabel(groupBox)
        labelDelete.setGeometry(QRect(295, 221, 140, 22))
        labelDelete.setText("[" + "<a href=#>Tüm Verileri Sil</a>" + "]")
        labelDelete.setFont(font)
        labelDelete.clicked.connect(self.deleteAllLogFolder)
        labelDelete.setObjectName("settingsMenu")

        labelDataLocal = WhiteLabel(groupBox)
        labelDataLocal.setGeometry(QRect(30, 251, 205, 22))
        labelDataLocal.setText("Kullanım Verileri Konumu:")
        labelDataLocal.setFont(font)
        labelDataLocal.setObjectName("settingsMenu")

        labelOpen = clickableLabel(groupBox)
        labelOpen.setGeometry(QRect(295, 251, 150, 22))
        labelOpen.setText("[" + "<a href=#>Veri Klasörünü Aç</a>" + "]")
        labelOpen.setFont(font)
        labelOpen.clicked.connect(self.openLogFolder)
        labelOpen.setObjectName("settingsMenu")

        okButton = PushButton(groupBox)
        okButton.setGeometry(QRect(30, 285, 141, 41))
        okButton.setText('TAMAM')
        okButton.setFont(font)
        okButton.setStyleSheet("QPushButton { color: white;padding: 5px;margin: 4px 2px;border-radius: 4px; background-color: rgb(0, 170, 255);} " \
                      "QPushButton::hover{background-color:rgb(4, 124, 184)}")
        okButton.setObjectName("settingsMenu")


        okButton.pressed.connect(self._okButton)
        self.loggingCase.stateChanged.connect(self.logging)
        self.checkExam.stateChanged.connect(self.examDataPermitControl)
        self.chatbotStatus.stateChanged.connect(self.chatbotControl)


        layout = QVBoxLayout()
        layout.addWidget(groupBox)
        self.setLayout(layout)
        self.center()

    def changeCodeFont(self):
        font = QFont()
        font.setFamily(self.c.getCodeFont())
        font.setPointSize(int(self.c.getFontSize()))

        font, ok = self.codeFontDialog.getFont(font, fontDialog(), "Font Ayarları", QFontDialog.MonospacedFonts)
        if ok:
            fontData = font.toString().split(',')
            self.c.setCodeFont(fontData[0])
            self.c.updateConfig('Size', 'size', str(round(float(fontData[1]))))
            self.codeBox.setText(self.c.getCodeFont())
            self.codeSizeBox.setText(str(self.c.getFontSize()))

    def changeEditorFont(self):
        try:
            font = QFont()
            font.setFamily(self.c.getEditorFont())
            font.setPointSize(self.c.getEditorFontSize())

            font, ok = self.editorFontDialog.getFont(font, fontDialog(), "Font Ayarları", QFontDialog.ProportionalFonts)
            if ok:
                fontData = font.toString().split(',')
                self.c.setEditorFont(fontData[0])
                self.c.updateConfig('Size', 'editorsize', str(round(float(fontData[1]))))
                self.editorBox.setText(self.c.getEditorFont())
                self.editorSizeBox.setText(str(self.c.getEditorFontSize()))
        except Exception as err:
            print("changeEditorFont {0}".format(err))


    def _okButton(self):
        CustomizeMessageBox_Ok("Bu ayarlarda yaptığınız değişiklikler Pynar Editörünü tekrar başlattığınızda geçerli olacaktır.", QMessageBox.Warning)
        self.close()

    def deleteAllLogFolder(self):
        try:
            mess = "Tüm Kullanım ve Hata Verileriniz Silinecek\n\t\"Onaylıyor musunuz ?\""
            CustomizeMessageBox_Yes_No(mess, clickAccept=self.yesButton)
        except Exception as err:
            print("deleteAllLogFolder {0}".format(err))

    def yesButton(self):
        logDir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))) + "/Log/"
        filelist = [f for f in os.listdir(logDir) if f.endswith(".json")]
        for f in filelist:
            os.remove(os.path.join(logDir, f))
        CustomizeMessageBox_Ok("Tüm Kullanım Verileri Silindi", QMessageBox.Information)


    def openLogFolder(self):
        try:
            if self.c.getSystem() == "windows":
                subprocess.call("explorer " + os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))) + "\Log", shell = True)
            elif self.c.getSystem() == "mac":
                os.system("open " + os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))) + "/Log")
            else:
                os.system("xdg-open " + os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))) + "/Log")

        except Exception as err:
            print("openLogFolder {0}".format(err))

    def logging(self):
        cs = bool(self.loggingCase.checkState())
        self.c.updateConfig('Logging', 'logging', str(cs))

    def chatbotControl(self):
        cs = bool(self.chatbotStatus.checkState())
        self.c.updateConfig('ChatbotStatus', 'ChatbotStatus', str(cs))

    def examDataPermitControl(self):
        cs = bool(self.checkExam.checkState())
        self.c.updateConfig('ExamLogging', 'ExamLogging', str(cs))

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

    def close(self):
        tab = self.tabWidthBox.value()
        self.c.updateConfig('Tab', 'tab', str(tab))
        self.done(1)

class clickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self,parent=None):
        super().__init__(parent)

    def mousePressEvent(self, ev):
        self.clicked.emit()
