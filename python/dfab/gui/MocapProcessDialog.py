# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MocapProcessDialog.ui'
#
# Created: Sat Feb 15 11:42:57 2014
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

class Ui_MocapProcessDialogWindow(object):
    def setupUi(self, MocapProcessDialogWindow):
        MocapProcessDialogWindow.setObjectName(_fromUtf8("MocapProcessDialogWindow"))
        MocapProcessDialogWindow.resize(579, 444)
        self.centralwidget = QtGui.QWidget(MocapProcessDialogWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.csvChooseButton = QtGui.QPushButton(self.centralwidget)
        self.csvChooseButton.setObjectName(_fromUtf8("csvChooseButton"))
        self.horizontalLayout_2.addWidget(self.csvChooseButton)
        self.csvName = QtGui.QLineEdit(self.centralwidget)
        self.csvName.setObjectName(_fromUtf8("csvName"))
        self.horizontalLayout_2.addWidget(self.csvName)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.paramsChooseButton = QtGui.QPushButton(self.centralwidget)
        self.paramsChooseButton.setObjectName(_fromUtf8("paramsChooseButton"))
        self.horizontalLayout_3.addWidget(self.paramsChooseButton)
        self.paramsName = QtGui.QLineEdit(self.centralwidget)
        self.paramsName.setObjectName(_fromUtf8("paramsName"))
        self.horizontalLayout_3.addWidget(self.paramsName)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.chooseTrajButton = QtGui.QPushButton(self.centralwidget)
        self.chooseTrajButton.setObjectName(_fromUtf8("chooseTrajButton"))
        self.horizontalLayout_4.addWidget(self.chooseTrajButton)
        self.trajName = QtGui.QLineEdit(self.centralwidget)
        self.trajName.setObjectName(_fromUtf8("trajName"))
        self.horizontalLayout_4.addWidget(self.trajName)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.bodyLabel = QtGui.QLabel(self.centralwidget)
        self.bodyLabel.setObjectName(_fromUtf8("bodyLabel"))
        self.horizontalLayout_5.addWidget(self.bodyLabel)
        self.bodyName = QtGui.QLineEdit(self.centralwidget)
        self.bodyName.setObjectName(_fromUtf8("bodyName"))
        self.horizontalLayout_5.addWidget(self.bodyName)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.convertButton = QtGui.QPushButton(self.centralwidget)
        self.convertButton.setObjectName(_fromUtf8("convertButton"))
        self.verticalLayout.addWidget(self.convertButton)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.consoleOutput = QtGui.QPlainTextEdit(self.centralwidget)
        self.consoleOutput.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.consoleOutput.setObjectName(_fromUtf8("consoleOutput"))
        self.gridLayout.addWidget(self.consoleOutput, 1, 0, 1, 1)
        MocapProcessDialogWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MocapProcessDialogWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 579, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuTitle = QtGui.QMenu(self.menubar)
        self.menuTitle.setObjectName(_fromUtf8("menuTitle"))
        self.menuSettings = QtGui.QMenu(self.menubar)
        self.menuSettings.setObjectName(_fromUtf8("menuSettings"))
        MocapProcessDialogWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MocapProcessDialogWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MocapProcessDialogWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuTitle.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())

        self.retranslateUi(MocapProcessDialogWindow)
        QtCore.QObject.connect(self.csvChooseButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MocapProcessDialogWindow.chooseCSVPath)
        QtCore.QObject.connect(self.paramsChooseButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MocapProcessDialogWindow.chooseParamsPath)
        QtCore.QObject.connect(self.chooseTrajButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MocapProcessDialogWindow.chooseTrajectoryPath)
        QtCore.QObject.connect(self.convertButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MocapProcessDialogWindow.convertTrajectory)
        QtCore.QMetaObject.connectSlotsByName(MocapProcessDialogWindow)

    def retranslateUi(self, MocapProcessDialogWindow):
        MocapProcessDialogWindow.setWindowTitle(_translate("MocapProcessDialogWindow", "Motion Capture Processor", None))
        self.csvChooseButton.setText(_translate("MocapProcessDialogWindow", "Choose CSV", None))
        self.paramsChooseButton.setText(_translate("MocapProcessDialogWindow", "Choose Params", None))
        self.chooseTrajButton.setText(_translate("MocapProcessDialogWindow", "Choose Trajectory", None))
        self.bodyLabel.setText(_translate("MocapProcessDialogWindow", "Body Name", None))
        self.convertButton.setText(_translate("MocapProcessDialogWindow", "Convert Trajectory", None))
        self.menuTitle.setTitle(_translate("MocapProcessDialogWindow", "File", None))
        self.menuSettings.setTitle(_translate("MocapProcessDialogWindow", "Settings", None))

