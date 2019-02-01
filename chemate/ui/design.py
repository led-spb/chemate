# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chemate\ui\design.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(530, 571)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.viewBoard = QtWidgets.QGraphicsView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.viewBoard.sizePolicy().hasHeightForWidth())
        self.viewBoard.setSizePolicy(sizePolicy)
        self.viewBoard.setMinimumSize(QtCore.QSize(530, 530))
        self.viewBoard.setLineWidth(1)
        self.viewBoard.setRenderHints(QtGui.QPainter.Antialiasing|QtGui.QPainter.HighQualityAntialiasing|QtGui.QPainter.TextAntialiasing)
        self.viewBoard.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        self.viewBoard.setObjectName("viewBoard")
        self.horizontalLayout.addWidget(self.viewBoard)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 530, 21))
        self.menubar.setObjectName("menubar")
        self.menuGame = QtWidgets.QMenu(self.menubar)
        self.menuGame.setObjectName("menuGame")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNewGame = QtWidgets.QAction(MainWindow)
        self.actionNewGame.setObjectName("actionNewGame")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.menuGame.addAction(self.actionNewGame)
        self.menuGame.addSeparator()
        self.menuGame.addAction(self.actionQuit)
        self.menubar.addAction(self.menuGame.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Chemate"))
        self.menuGame.setTitle(_translate("MainWindow", "Game"))
        self.actionNewGame.setText(_translate("MainWindow", "New..."))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))

