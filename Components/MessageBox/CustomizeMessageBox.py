from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui

from configuration import Configuration


def CustomizeMessageBox_Yes_No(message, clickAccept=None, clickCancel=None):
    c = Configuration()
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Question)
    msgBox.setWindowTitle('Pynar Mesaj Kutusu')
    msgBox.setWindowIcon(QIcon(':/icon/images/headerLogo1.png'))
    msgBox.setText(message)
    msgBox.setWindowFlags(msgBox.windowFlags() | Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
    msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    font = QFont()
    font.setFamily(c.getEditorFont())
    font.setPointSize(c.getHistoryMenuFontSize() + 6)
    msgBox.setFont(font)
    msgBox.setStyleSheet(open(c.getHomeDir() + "qssfiles/qmessagebox.qss", "r").read())
    BtnOk = msgBox.button(QMessageBox.Ok)
    msgBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    BtnOk.setText('Evet')
    if clickAccept:
        msgBox.accepted.connect(clickAccept)
    if clickCancel:
        msgBox.rejected.connect(clickCancel)
    BtnCancel = msgBox.button(QMessageBox.Cancel)
    BtnCancel.setText('Hayır')
    msgBox.exec()


def CustomizeMessageBox_Ok(message, icon):
    c = Configuration()
    msgBox = QMessageBox()
    msgBox.setIcon(icon)
    msgBox.setText(message)
    msgBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    msgBox.setWindowTitle('Pynar Mesaj Kutusu')
    msgBox.setWindowIcon(QIcon(':/icon/images/headerLogo1.png'))
    msgBox.setWindowFlags(msgBox.windowFlags() | Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
    msgBox.setStandardButtons(QMessageBox.Ok)
    font = QFont()
    font.setFamily(c.getEditorFont())
    font.setPointSize(c.getHistoryMenuFontSize() + 6)
    msgBox.setFont(font)
    msgBox.setStyleSheet(open(c.getHomeDir() + "qssfiles/qmessagebox.qss", "r").read())
    BtnOk = msgBox.button(QMessageBox.Ok)
    BtnOk.setText('Tamam')
    msgBox.exec()


