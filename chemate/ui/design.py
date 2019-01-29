# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(576, 496)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.viewBoard = QtWidgets.QGraphicsView(self.centralwidget)
        self.viewBoard.setMinimumSize(QtCore.QSize(256, 256))
        self.viewBoard.setObjectName("viewBoard")
        self.horizontalLayout.addWidget(self.viewBoard)
        self.listView = QtWidgets.QListView(self.centralwidget)
        self.listView.setMaximumSize(QtCore.QSize(150, 16777215))
        self.listView.setObjectName("listView")
        self.horizontalLayout.addWidget(self.listView)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 576, 21))
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

