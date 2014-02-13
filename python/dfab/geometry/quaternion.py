"""Ad-hoc implementation of quaternion operators using numpy.

Copyright (c) 2014, Garth Zeglin.  All rights reserved. Licensed under the terms
of the BSD 3-clause license as included in LICENSE.

All quaternions are represented as a 4 element numpy ndarray, following a (w,x,y,z) convention.

All operators are pure Python for portability.

N.B. this is not well tested, efficient, or optimized.

Quaternion addition is just the usual vector sum: q1 + q2

"""

import numpy as np

def axis_angle( axis, angle ):
    """Return the quaternion corresponding to a rotation around an axis.

    Arguments: (axis, angle)
    axis  -- three element vector
    angle -- scalar representing an angle in radians.
    """

    # the scale factor normalizes the axis vector and multiplies by half the sine in one step
    scale = np.sin( angle / 2 ) / np.sqrt(np.dot(axis, axis))
    return np.array(( np.cos(angle/2), scale*axis[0], scale*axis[1], scale*axis[2] ))


def vector( v ):
    """Return the quaternion representing a three-element vector."""
    return np.array(( 0, v[0], v[1], v[2] ))


def identity():
    """Return an identity quaternion representing no rotation."""
    return np.array(( 1.0, 0.0, 0.0, 0.0 ))


def normalize( q ):
    """Return a properly normalized quaternion.

    Rotation quaternions have unit magnitude, but numerical error can accumulate.
    """

    mag = np.sqrt( np.dot(q,q) )
    if mag == 0:
        return identity()
    else:
        return q / mag


def conjugate( q ):
    """Return the conjugate of a quaternion."""
    return np.array(( q[0], -q[1], -q[2], -q[3] ))


def multiply( p, q ):
    """Compute the quaternion product p*q.

    The product  p * q  = p0q0 - p.q + p0 q + q0 p + p X q
    """
    return np.array ((  p[0] * q[0] - p[1] * q[1] -  p[2] * q[2] - p[3] * q[3], 
                        p[0] * q[1] + p[1] * q[0] + (p[2] * q[3])-(p[3] * q[2]), 
                        p[0] * q[2] + p[2] * q[0] + (p[3] * q[1])-(p[1] * q[3]), 
                        p[0] * q[3] + p[3] * q[0] + (p[1] * q[2])-(p[2] * q[1]) ))


def rotate_vector( q, v ):
    """Rotate a three-element vector v by the orientation represented by quaternion q.

    Arguments: (q, v)
    Returns a new vector.
    """

    r = multiply( multiply(q, vector(v)), conjugate( q ))
    return r[1:4]


def to_threexform( q ):
    """Return a 4x4 homogenous matrix representing a quaternion rotation."""

    # this should be fixed to work with a matrix of quaternions
    return np.array( (( q[0]*q[0]+q[1]*q[1]-q[2]*q[2]-q[3]*q[3],
                        2*(q[1]*q[2]-q[0]*q[3]),
                        2*(q[1]*q[3]+q[0]*q[2]),
                        0.0 ),

                      ( 2*(q[1]*q[2]+q[0]*q[3]),
                        q[0]*q[0]-q[1]*q[1]+q[2]*q[2]-q[3]*q[3],
                        2*(q[2]*q[3]-q[0]*q[1]),
                        0.0 ),

                      ( 2*(q[1]*q[3]-q[0]*q[2]),
                        2*(q[2]*q[3]+q[0]*q[1]),
                        q[0]*q[0]-q[1]*q[1]-q[2]*q[2]+q[3]*q[3],
                        0.0 ),
                      
                      ( 0, 0, 0, 1 ) ))

