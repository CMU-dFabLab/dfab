"""Simple utility functions for geometric data."""

import numpy as np

# local to this package
import quaternion as quat
import threexform as xform

# ==================================================================
def xyzw_to_wxyz( q ):
    """Convert (x, y, z, w) quaternions returned by the mocap system to (w,x,y,z) order as used by the quaternion code.
    
    Arguments:
    q -- N x 4 list of 4-element quaternions or single quaternion

    """
    if len(q.shape)==2:
        return np.vstack( (q[:,3],q[:,0],q[:,1],q[:,2])).transpose()
    else:
        return np.array((q[3], q[0], q[1], q[2] ))

# ==================================================================

def pos_quat_to_threexform( x, q ):
    """Generate a homogeneous transform from a position vector and a quaternion."""
    tq = quat.to_threexform( q )
    tq[0:3,3] = x  # directly set the translation vector portion of the transform
    return tq


def pos_ypr_to_threexform( x, ypr ):
    """Generate a homogeneous transform from a position vector and a (yaw, pitch, roll) triple.
    Note: (yaw, pitch, roll) are assumed to be in *degrees* in this library.
    """

    tq = xform.yaw_pitch_roll( ypr[0], ypr[1], ypr[2] )
    tq[0:3,3] = x  # directly set the translation vector portion of the transform
    return tq

# ==================================================================
