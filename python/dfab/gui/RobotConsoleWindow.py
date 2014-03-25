# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RobotConsoleWindow.ui'
#
# Created: Mon Feb 17 19:01:53 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_RobotConsoleWindow(object):
    def setupUi(self, RobotConsoleWindow):
        RobotConsoleWindow.setObjectName(_fromUtf8("RobotConsoleWindow"))
        RobotConsoleWindow.resize(812, 631)
        self.centralwidget = QtGui.QWidget(RobotConsoleWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.openGLviewLayout = QtGui.QHBoxLayout()
        self.openGLviewLayout.setObjectName(_fromUtf8("openGLviewLayout"))
        self.verticalLayout.addLayout(self.openGLviewLayout)
        self.consoleOutput = QtGui.QPlainTextEdit(self.centralwidget)
        self.consoleOutput.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.consoleOutput.setObjectName(_fromUtf8("consoleOutput"))
        self.verticalLayout.addWidget(self.consoleOutput)
        self.buttonLayout = QtGui.QHBoxLayout()
        self.buttonLayout.setObjectName(_fromUtf8("buttonLayout"))
        self.verticalLayout.addLayout(self.buttonLayout)
        self.commandLine = QtGui.QLineEdit(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.commandLine.sizePolicy().hasHeightForWidth())
        self.commandLine.setSizePolicy(sizePolicy)
        self.commandLine.setObjectName(_fromUtf8("commandLine"))
        self.verticalLayout.addWidget(self.commandLine)
        RobotConsoleWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(RobotConsoleWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 812, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuTitle = QtGui.QMenu(self.menubar)
        self.menuTitle.setObjectName(_fromUtf8("menuTitle"))
        self.menuSettings = QtGui.QMenu(self.menubar)
        self.menuSettings.setObjectName(_fromUtf8("menuSettings"))
        RobotConsoleWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(RobotConsoleWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        RobotConsoleWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuTitle.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())

        self.retranslateUi(RobotConsoleWindow)
        QtCore.QObject.connect(self.commandLine, QtCore.SIGNAL(_fromUtf8("returnPressed()")), RobotConsoleWindow.commandEntered)
        QtCore.QMetaObject.connectSlotsByName(RobotConsoleWindow)

    def retranslateUi(self, RobotConsoleWindow):
        RobotConsoleWindow.setWindowTitle(_translate("RobotConsoleWindow", "Robot Console", None))
        self.menuTitle.setTitle(_translate("RobotConsoleWindow", "File", None))
        self.menuSettings.setTitle(_translate("RobotConsoleWindow", "Settings", None))

