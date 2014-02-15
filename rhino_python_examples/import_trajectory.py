"""Example code for importing trajectories into Rhino.

Copyright (c) 2014, Garth Zeglin.  All rights reserved. Licensed under the terms
of the BSD 3-clause license as included in LICENSE.

Example code for generating a path of Rhino 'planes' (e.g. coordinate frame)
from a trajectory data file.  The path is returned as a list of Plane objects.

Each plane is created using an origin vector and X and Y basis vectors.  The
time stamps and Z basis vectors in the trajectory file are ignored.

Inputs visible in Grasshopper:
  library_path --- full path to dFab Python library

Outputs visible in Grasshopper:
  a  -- the list of planes
"""

# set the following true if debugging outside of Rhino
# no_rhino = True
no_rhino = False

import sys
import os

# set up the Python load path to find the dFab library
sys.path.append( library_path )

import dfab
import dfab.mocap.datafiles as datafiles

# if debugging without Rhino, import the trivial emulation module
if no_rhino:
    import dfab.debug.rhinoscriptsyntax as rs
else:
    import rhinoscriptsyntax as rs

# Look for the data file in the sample data folder.
# N.B. this assumes that the dfab and dfab-data packages are installed in the same folder!
# This is reaching outside the dfab package proper.
filename = os.path.join( dfab.dfab_package_path(), "../dfab-data/motion_capture_example/2014-01-17-Wall-Sweep-with-Robot.traj" )

# load the trajectory data
path, timestamps = datafiles.read_frame_trajectory_file( filename )

# Create a list of Rhino 'plane' objects to return as a path.
planes = []

# Each Rhino 'plane' is constructed from an origin and two basis vectors using
# PlaneFromFrame. Syntax of the PlaneFromFrame operator:
# rs.PlaneFromFrame (origin, x_axis, y_axis)

for f in path:
    origin = f[0]
    xaxis  = f[1]
    yaxis  = f[2]
    planes.append( rs.PlaneFromFrame( origin, xaxis, yaxis ))

# Return the list in a global variable exposed in the Grasshopper interface.
a = planes

# If not running in Rhino, provide some debug output.
if no_rhino:
    import numpy as np
    # use a more readable numpy output format
    np.set_printoptions(suppress=True, precision=5)
    print "Trajectory:\n"
    for time,frame in zip(timestamps, planes):
        print "Time:", time, "\n", frame
