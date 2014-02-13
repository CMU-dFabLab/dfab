"""Functions for creating and manipulating homogeneous transforms using numpy.

Copyright (c) 2014, Garth Zeglin.  All rights reserved. Licensed under the terms
of the BSD 3-clause license as included in LICENSE.

- All transforms are represented as a full 4x4 numpy ndarray.
- All operators are pure Python for portability.
- Transform composition is just normal matrix multiplication: numpy.dot(m1, m2).

N.B. this is not well tested, efficient, or optimized.

"""

import numpy as np

def rotation_x( angle ):
    """Return a homogeneous 4x4 transform to rotate 'angle' radians around X."""
    sinval = np.sin( angle )
    cosval = np.cos( angle )
    M = np.identity( 4 )
    M[1][1] = cosval;      M[1][2] = -sinval
    M[2][1] = sinval;      M[2][2] =  cosval
    return M

def rotation_y( angle ):
    """Return a homogeneous 4x4 transform to rotate 'angle' radians around Y."""
    sinval = np.sin( angle )
    cosval = np.cos( angle )
    M = np.identity( 4 )
    M[0][0] = cosval;       M[0][2] = sinval
    M[2][0] = -sinval;      M[2][2] = cosval
    return M

def rotation_z( angle ):
    """Return a homogeneous 4x4 transform to rotate 'angle' radians around Z."""
    sinval = np.sin( angle )
    cosval = np.cos( angle )
    M = np.identity( 4 )
    M[0][0] = cosval;     M[0][1] = -sinval
    M[1][0] = sinval;     M[1][1] =  cosval
    return M

def translation( x, y, z ):
    """Return a homogeneous 4x4 transform to translate along the given vector specified as individual components."""
    M = np.identity( 4 )
    M[0:3,3] = (x, y, z)
    return M

deg_to_rad = np.pi / 180.0

def yaw_pitch_roll( yaw, pitch, roll ):
    """Return a homogeneous 4x4 transform representing a rotation specified by a
    set of ZYX Euler angles (yaw-pitch-roll) **specified in degrees**. 

    The angles are specified in degrees because YPR are generally assumed to be
    provided for human readability.
    """
    return rotation_z( yaw * deg_to_rad ).dot( rotation_y( pitch * deg_to_rad ).dot ( rotation_x( roll * deg_to_rad )))

################################################################

if __name__ == "__main__":
    """Run some trivial tests when executed as a main module."""
    np.set_printoptions(suppress=True, precision=5)

    # In a homogeneous transform matrix premultiplying a vector in a rotated
    # frame, the columns of the upper-left 3x3 rotation submatrix specify the
    # unit axis vectors of the rotated frame in world coordinates.  This can be
    # used to check the matrices by inspection.
    print "small x rotationa:\n", rotation_x( 0.1 )
    print "small y rotation:\n",  rotation_y( 0.1 )
    print "small z rotation:\n",  rotation_z( 0.1 )
    print "small translation:\n", translation( 0.1, 0.2, 0.3 )

    print "translate then rotate:\n", translation( [0.1,0.2,0.3] ).dot( rotation_x(0.1))
    print "rotate then translate:\n", rotation_x(0.1).dot( translation( 0.1,0.2,0.3 ))
    print "applied to a point:\n", rotation_x(0.1).dot( translation( 0.1, 0.2, 0.3 )).dot([1,2,3,1])

    halfpi =  0.5*np.pi
    print "90 degree X rotation:\n", rotation_x( 0.5*np.pi )
    print "90 degree Y rotation:\n", rotation_y( 0.5*np.pi )
    print "90 degree Z rotation:\n", rotation_z( 0.5*np.pi )

    # In the following example:
    #   rotated X should point along world -Z
    #   rotated Y should point along world -X 
    #   rotated Z should point along world  Y 
    print "yaw-pitch-roll Euler angles for yaw 90 degrees, pitch 90 degrees:\n", yaw_pitch_roll( 90.0, 90.0, 0.0 )
