"""Forward kinematic calculations for the ABB 6640 on a track.

ABB6640/parameters.py, Copyright (c) 2013-2014 Garth Zeglin. All rights
reserved. Licensed under the terms of the BSD 3-clause license as included in
LICENSE.

N.B. These have not been checked in detail.
"""
import math
import numpy as np
from dfab.ABB6640.parameters import *
from dfab.geometry.transform3d import *

#================================================================
def tcp( track, a1, a2, a3, a4, a5, a6 ):
    """Compute the homogeneous transform representing the default TCP (tool center
    point) frame for the given kinematic state.

    The track location is specified in meters.
    The arm joint angles are specified in radians.
    """
    
    m = Transform3D()
    
    m.translate( track, 0.0, track_z_offset ) # track translation along X, vertical offset along Z
    m.rotate_z ( a1 )      	              # axis 1 rotation around Z
    m.translate( axis_2_x, 0.000, axis_2_z)   # axis 2 forward of origin and above top of track
    m.rotate_y ( a2 )  	                      # axis 2 rotation around Y
    m.translate( 0.000, 0.000, axis_3_z )     # axis 3 above axis 2
    m.rotate_y ( a3 )  	                      # axis 3 rotation around Y
    m.translate( wrist_x, 0.000, wrist_z )    # wrist center above and in front of axis 2
    m.rotate_x ( a4 )  	                      # axis 4 rotation around X
    m.rotate_y ( a5 )  	                      # axis 5 rotation around Y
    m.rotate_x ( a6 )  	                      # axis 6 rotation around X
    m.rotate_y ( math.pi/2 )        	      # rotate +Z down along +X
    m.translate( 0.000, 0.000, endplate_x )   # flange in front of wrist center

    return m.ctm

#================================================================
