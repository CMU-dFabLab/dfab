"""Essential kinematic dimensions and motion limits for the ABB 6640 on a track.

ABB6640/parameters.py, Copyright (c) 2013-2014 Garth Zeglin. All rights
reserved. Licensed under the terms of the BSD 3-clause license as included in
LICENSE.

N.B. These have not been checked in detail.
"""
import math
import numpy as np

#================================================================
# Dimensional constants. Most are taken from ABB document 3HAC028284-001 Ref F page 13.

# These define the axis relationships and must be exact.
track_z_offset = 0.300  # track height, estimated
axis_2_x       = 0.320  # axis 2 distance forward of robot origin
axis_2_z       = 0.780  # axis 2 height above robot origin
axis_3_z       = 1.075  # axis 3 height above axis 2 (G on drawing, either 1.075 or 1.280, depending on model)
wrist_x        = 1.142  # wrist center distance forward of axis 3 (D on drawing, either 1.142, 1.392, or 1.592)
wrist_z        = 0.200  # wrist center height above axis 3
endplate_x     = 0.200  # endplate center in front of wrist center

################################################################
def degtorad(deg):
    return deg * (math.pi / 180.0)

# Joint position limits.
pos_max = np.array( [ 6.9 ] + [ degtorad(angle) for angle in [  170,  85,   70,  300,  120,  360 ]] )
pos_min = np.array( [ 0.0 ] + [ degtorad(angle) for angle in [ -170, -65, -180, -300, -120, -360 ]] )

# Joint velocity limits.  The arm speed limits are the conservative bounds, the
# actual limits can be slightly higher in some poses.

# @bug The min/max track velocity is speculative.

vel_max = np.array( [ 0.5 ] + [ degtorad(angle) for angle in [ 100, 90, 90, 170, 120, 190 ]] )
vel_min = -vel_max

################################################################
