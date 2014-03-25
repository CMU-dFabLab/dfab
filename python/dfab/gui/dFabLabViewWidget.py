"""PyQt OpenGL widget for rendering a view of the dFab Lab, managing the camera
and drawing the fixed geometry with default lighting.

dFabLabViewWidget.py, Copyright (c) 2013-2014, Garth Zeglin. All rights
reserved. Licensed under the terms of the BSD 3-clause license as included in
LICENSE.

This does not actually draw the mobile hardware, it is intended to be subclasses
for specific applications.  This can be easily installed in the RobotConsole
OpenGL 3D view during initialization.
"""

from PyQt4 import QtGui
from RobotConsole import *
import sys

from PyQt4.QtOpenGL import *
from OpenGL.GL import *

import gl_camera
import gl_drawing

################################################################


class dFabLabViewWidget(QGLWidget):
    """A rendering of a lab room with a Robot6640 robot on a track.

    The view handles mouse inputs as camera controls.
    """

    def __init__(self, parent = None):
        super(dFabLabViewWidget, self).__init__(parent)
        self.setMinimumWidth ( 640 )
        self.setMinimumHeight( 480 )
        # self.setMouseTracking ( True )
        self.camera = gl_camera.camera()
        self.timer = None

    def timerTick( self ):
       """Overridable default method for processing timer callbacks which does nothing.
       Typically a subclass implementation of this method will update view
       animation state and then call self.updateGL() to invoke the QGLWidget
       method that will initiate a redraw of the view.
       """
       pass

    def startFrameTimer( self, interval = 40 ):
       """Start a periodic timer which will call the timerTick() method at fixed
       intervals specified in milliseconds."""
       self.timer = QtCore.QTimer()
       QtCore.QObject.connect( self.timer, QtCore.SIGNAL("timeout()"), self.timerTick )
       self.timer.start( int(interval) )  # interval in milliseconds
       return

    def mouseMoveEvent( self, mouse ):
        self.camera.mouse_drag_around_fixation( mouse.x(), mouse.y() )
        self.updateGL()

    def mousePressEvent( self, mouse ):
        # on the mac:
        #   the 'command' key is the ControlModifier
        #   the 'control' key selects button-2 and is MetaModifier
        #   the 'option' key is the AltModifier
        # more masks QtCore.Qt.AltModifier QtCore.Qt.MetaModifier
        modifiers = mouse.modifiers()
        shift   = int(modifiers & QtCore.Qt.ShiftModifier) != 0
        control = int(modifiers & QtCore.Qt.ControlModifier) != 0
        left  = (mouse.button() == 1)
        right = (mouse.button() == 2)
        self.camera.mouse_down( mouse.x(), mouse.y(), left = left, shift = shift, control = control )

    def mouseReleaseEvent( self, mouse ):
        pass

    def drawRobot( self ):
        """Overridable default function to draw the robot system."""
        pass

    def paintGL(self):
        glClearColor( 0.0, 0.2, 0.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        self.camera.set_current_transform()
        glPolygonMode( GL_BACK, GL_LINE )

        gl_drawing.gl_draw_checkerboard_ground_plane( -3, -3,  13.0, 3, 0.8, 0.2 )
        gl_drawing.gl_init_default_lighting()
        self.drawRobot()
        return

    def resizeGL(self, w, h):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-50, 50, -50, 50, -50.0, 50.0)
        glViewport(0, 0, w, h)
        return

    def initializeGL(self):
        """This is called once before the first resizeGL or paintGL."""
        pass

################################################################
