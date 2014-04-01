"""Generate ABB RAPID program fragments to follow a fixed trajectory of joint-space poses.

Copyright (c) 2013-2014, Garth Zeglin.  All rights reserved. Licensed under the terms
of the BSD 3-clause license as included in LICENSE.

RAPID programs are returned as strings.  Lines are terminated with CR-LF. 
The robot platform is assumed to be a six-axis ABB 6640 on a track.
"""

import math
import time

## Convert a value from radians to degrees.  The ABB RAPID joint targets are defined in degrees.
def r2d( radians ):
    return radians * ( 180.0 / math.pi )

def joint_targets( data, robot='ABB6640', a_unit='degree', l_unit='mm', first=0, base='pose', prefix='   ', **kwargs ):
    """Return a set of joint target definitions given a sequence of seven-element
    sequences of joint angles, All joint angles are defined in kinematic order,
    e.g., the track position is first, followed by six arm angles.  All angles
    are in radians, the track position is in meters.  Note that these values are
    scaled to degrees and millimeters in the output.

    Arguments:
    data    sequence of joint sequences
    robot   string identifying the target robot (default is ABB6640)
    a_unit  string identifying the angular units in which the joints are specified (degree or radian, default is degree)
    l_unit  string identifying the linear units in which the joints are specified (meter or mm, default is mm)
    first   numerical index of first defined target (default is 0)
    base    base name for targets (default is 'pose')
    prefix  prefix string for each line (default is three spaces)
    """

    # this could extend to other machines, but for now it is just the one
    assert( robot == 'ABB6640' )

    elements = list()
    index = first
    for pose in data:
        track = (1000.0 * pose[0]) if l_unit == 'meter' else (pose[0])
        if a_unit == 'radian':
            elements.append( prefix + "CONST jointtarget %s%d := [[%9.4f,%9.4f,%9.4f,%9.4f,%9.4f,%9.4f],[%9.3f,9E9,9E9,9E9,9E9,9E9]];\r\n" % \
                             ( base, index, r2d(pose[1]), r2d(pose[2]), r2d(pose[3]), r2d(pose[4]), r2d(pose[5]), r2d(pose[6]), track ))
        elif a_unit == 'degree':
            elements.append( prefix + "CONST jointtarget %s%d := [[%9.4f,%9.4f,%9.4f,%9.4f,%9.4f,%9.4f],[%9.3f,9E9,9E9,9E9,9E9,9E9]];\r\n" % \
                             ( base, index, pose[1], pose[2], pose[3], pose[4], pose[5], pose[6], track ))
        index += 1

    comment = prefix + "! Define a sequence of joint-space poses.  Format is  [[arm0...], [track, ...]]  Angles are in degrees, track position in millimeters.\r\n"
    return comment + "".join( elements )

#================================================================
def joint_moves( times, robot='ABB6640', first=1, base='pose', prefix = '      ', **kwargs):
    """Return a set of joint-space move commands given a sequence of move durations.
    This references a previously defined set of joint target definitions.
    Move durations are in seconds.

    Arguments:
    times   sequence of move durations
    robot   string identifying the target robot (default is ABB6640)
    first   numerical index of first defined target (default is 1)
    base    base name for targets (default is 'pose')
    prefix  prefix string for each line (default is six spaces)
    """

    # this could extend to other machines, but for now it is just the one
    assert( robot == 'ABB6640' )

    elements = list()
    index = first
    for t in times:
        elements.append( prefix + "MoveAbsJ %s%d, v200\T:=%6.3f, z1, tool0\WObj:=wobj0;\r\n" % ( base, index, t ) )
        index += 1

    comment = prefix + "! Sequence of joint-space moves with specified durations.\r\n"
    return comment + "".join( elements )

# ###############################################################
def absolute_to_intervals ( times ):
    """Calculate a list of intervals from a list of absolute time points.  Note that
    there must be at least two time points, the points must be monotonically
    increasing, and the returned list will have one fewer elements.
    """
    # This does a pair-wise subtraction between the list starting at element 1 and the list starting at element 0.
    return map (lambda t1, t0: t1 - t0, times[1:], times[0:-1] )

# ###############################################################
def single_trajectory_program( trajectory, robot='ABB6640', module="sequence", proc="seqmove", **kwargs ):
    """Generate an entire RAPID program module to perform a fixed joint-space
    trajectory.  The trajectory is specified as a sequence of elements of the
    form [t, [joints]].  [joints] is a seven-element joint sequence starting with
    the track position.  Angles are in radians, distances in meters.  The program
    is returned as a string.  

    The program assumes that the robot is physically positioned at the initial
    configuration.  For safety, it issues a fixed-speed move to this location,
    but that command normally should have no effect.
    """

    # this could extend to other machines, but for now it is just the one
    assert( robot == 'ABB6640' )

    comment = "! Generated by rapid.single_trajectory_program() at %s\r\n" % time.ctime()
    return "MODULE %s\r\n" % module + \
        comment + \
        joint_targets( [ pt[1] for pt in trajectory ], **kwargs ) + \
        "   PROC %s()\r\n" % proc + \
        "      ! Safety move to start point.\r\n" + \
        "      MoveAbsJ pose0, v100, fine, tool0\Wobj:=wobj0;\r\n" + \
        joint_moves( absolute_to_intervals( [ pt[0] for pt in trajectory] ), **kwargs) + \
        "   ENDPROC\r\nENDMODULE\r\n"

# ###############################################################
# test entry point when running as a script
if __name__ == "__main__":
    data = [ [0.0,   [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0  ]],  
             [1.0,   [ 1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0  ]],
             [1.5,   [ 1.2,  0.0,  0.1, -0.1,  0.0,  0.0,  0.0  ]],
             [1.75,  [ 1.3,  0.0,  0.1, -0.1,  0.0,  0.0,  0.2  ]],
    ]

    print single_trajectory_program( data, a_unit = 'radian', l_unit = 'meter' )

# ###############################################################

