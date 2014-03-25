"""Convenience class for holding a single homogeneous transform and operating on it in-place.  This
is similar to the use of the current transformation matrix in OpenGL..

transform3d.py, Copyright (c) 2014 Garth Zeglin. All rights reserved. Licensed
under the terms of the BSD 3-clause license as included in LICENSE.
"""

import numpy as np
from dfab.geometry.threexform import *

#================================================================
class Transform3D:
    """Convenience class for holding a single homogeneous transform representing a
    coordinate frame and operating on it in-place.  This is similar to the use
    of the current transformation matrix in OpenGL.

    Each operation modifies the transformation state and returns the object
    itself to allow sequential composition, e.g.

    Transform3D().translate(x,y,z).rotate_x( angle).rotate_y(angle)

    Attributes:
    ctm -- the 4x4 homogenous transform

    Methods:
    translate( x,y,z )
    rotate_x( angle )
    rotate_y( angle )
    rotate_z( angle )
    set_identity()

    """

    def __init__(self):
        self.ctm = np.identity(4)
        return

    def set_identity(self):
        self.ctm = np.identity(4)
        return self

    def translate( self, x, y, z ):
        self.ctm = np.dot( self.ctm, translation( x, y, z ) )
        return self

    def rotate_x( self, angle ):
        self.ctm = np.dot( self.ctm, rotation_x( angle ))
        return self

    def rotate_y( self, angle ):
        self.ctm = np.dot( self.ctm, rotation_y( angle ))
        return self

    def rotate_z( self, angle ):
        self.ctm = np.dot( self.ctm, rotation_y( angle ))
        return self

#================================================================
