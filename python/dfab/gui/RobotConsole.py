"""PyQt window with 3D OpenGL view, command line, text console output, and
generic buttons, intended to act as robot control console.

RobotConsole.py, Copyright (c) 2013-2014, Garth Zeglin. All rights
reserved. Licensed under the terms of the BSD 3-clause license as included in
LICENSE.

This is suitable to be a parent class specialized by the user for a specific
application; the goal is to provide a simple generic interface.

"""
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

from PyQt4.QtOpenGL import *
from OpenGL.GL import *

from RobotConsoleWindow import *

################################################################
# Define a custom window which inherits both from the QMainWindow class
# and the custom Ui_RobotConsoleWindow defined in Qt Designer.

class RobotConsole( QtGui.QMainWindow, Ui_RobotConsoleWindow ):
    def __init__( self, view = None):
        QtGui.QMainWindow.__init__( self )
        self.setupUi( self )

        if view:
            glwidget = view
        else:
            glwidget = dFabLabViewWidget()
        self.openGLviewLayout.addWidget( glwidget )
        glwidget.show()

        return

    def consoleprint( self, string ):
        self.consoleOutput.appendPlainText( string )

    def commandEntered( self ):
        """Slot called when command line text is entered."""
        command = self.commandLine.text()
        self.commandLine.clear()
        self.consoleprint( 'User entered: "' + command + '"' )
        return

    def addButton( self, title, callback ):
        newButton = QtGui.QPushButton(self.centralwidget)
        newButton.setObjectName(_fromUtf8( title ))
        self.buttonLayout.addWidget( newButton )
        newButton.setText( title )
        QtCore.QObject.connect( newButton, QtCore.SIGNAL(_fromUtf8("clicked()")), callback )
        return

    def addSlider( self, title, callback ):
        """Add a horizontal slider to the controls area.  The range is fixed over [0,
        10000).  The user callback receives an integer value within this range
        during slider motion.
        """

        newSlider = QtGui.QSlider(self.centralwidget)
        newSlider.setOrientation(QtCore.Qt.Horizontal)
        newSlider.setObjectName(_fromUtf8( title ))
        self.buttonLayout.addWidget( newSlider )

        # This sets a fixed maximum larger than any current screen resolution; the user can scale to what they require.
        newSlider.setMaximum( 10000 )

        # this slider does not itself have text, so this sets a tooltip for it
        newSlider.setToolTip( "<html><head/><body><p>%s</p></body></html>" % title )

        QtCore.QObject.connect( newSlider, QtCore.SIGNAL(_fromUtf8("sliderMoved(int)")), callback )
        return

################################################################
