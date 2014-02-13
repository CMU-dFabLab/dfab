"""Prototype script to extract a trajectory data file from a Optitrack motion capture .csv file. 

Copyright (c) 2014, Garth Zeglin.  All rights reserved. Licensed under the terms
of the BSD 3-clause license as included in LICENSE.

This is still a long way from being a robust general-purpose program.
"""

import os
import math
import numpy as np
import dfab.mocap.optitrack_csv as optitrack
import dfab.mocap.datafiles as datafiles

import dfab.geometry.quaternion as quat
import dfab.geometry.threexform as xform

# use a more readable numpy output format
np.set_printoptions(suppress=True, precision=5)

data_folder_name = "../../dfab-data/motion_capture_example"
csv_file_name    =  "2014-01-17-Wall-Sweep-with-Robot.csv"
base_name        = os.path.splitext( csv_file_name )[0]
gen_debug_files  = False

data = optitrack.Run()
data.ReadFile( data_dir = data_folder_name, filename = csv_file_name, verbose = False )

print "Found %d rigid bodies, %d frames." % (data.trackablecount, data.framecount )
print "Bodies:",[body.name for body in data.trackables]

# ==================================================================
# Extract three lists of vectors defining the tool motion:
# timestamps, positions, and orientation quaternions.q
times, x_tool, q_tool, ypr_tool = data.trajectory('Small Tool')

# use a Python slice with a step index to subsample the input.
decimation_rate = 12
# decimation_rate = 100
times     = times[::decimation_rate]
x_tool    = x_tool[::decimation_rate]
q_tool    = q_tool[::decimation_rate]
ypr_tool  = ypr_tool[::decimation_rate]

# print "Euler angles for tool:\n", ypr_tool

################################################################
def xyzw_to_wxyz( q ):
    """Convert (x, y, z, w) quaternions returned by the mocap system to (w,x,y,z) order as used by the quaternion code.
    
    Arguments:
    q -- N x 4 list of 4-element quaternions or single quaternion

    """
    if len(q.shape)==2:
        return np.vstack( (q[:,3],q[:,0],q[:,1],q[:,2])).transpose()
    else:
        return np.array((q[3], q[0], q[1], q[2] ))


################################################################
# Convert the (x, y, z, w) quaternions returned by the mocap system to (w,x,y,z)
# order as used by the quaternion code.
q_tool = xyzw_to_wxyz(q_tool)

# Convert from the mocap default meter coordinates to millimeters
# for consistency with the ABB robot.
x_tool *= 1000

# Emit raw origin track for testing.
if gen_debug_files:
    print "Generating raw origin point track file."
    datafiles.write_point_trajectory_file( "plots/points.dat", times, x_tool )

# ==================================================================
# Generate a homogeneous transform representing each tool frame.
def make_threexform_from_pos_quat( x, q ):
    tq = quat.to_threexform( q )
    tq[0:3,3] = x  # directly set the translation vector portion of the transform
    return tq

# Generate a homogeneous transform representing each tool frame.
def make_threexform_from_pos_ypr( x, ypr ):
    tq = xform.yaw_pitch_roll( ypr[0], ypr[1], ypr[2] )
    tq[0:3,3] = x  # directly set the translation vector portion of the transform
    return tq

tool_traj = [ make_threexform_from_pos_quat( position, orientation ) for (position, orientation) in zip( x_tool, q_tool) ]
# tool_traj = [ make_threexform_from_pos_ypr( position, orientation ) for (position, orientation) in zip( x_tool, ypr_tool ) ]

# Write out the raw trajectory data for testing.
if gen_debug_files:
    print "Generating raw trajectory frame file."
    datafiles.write_frame_trajectory_file( "plots/raw.dat", times, tool_traj )

# ==================================================================
# Generate a homogeneous transform representing the ground marker in mocap coordinates.
# This assumes the marker didn't move and just averages over all components.  
# Convert from meters to millimeters.
t_ground, x_ground, q_ground, ypr_ground = data.trajectory('Ground')
x_gnd_avg = 1000.0 * np.mean( x_ground, axis=0 )
q_gnd_avg = xyzw_to_wxyz( quat.normalize(np.mean( q_ground, axis=0 )))

ground = make_threexform_from_pos_quat( x_gnd_avg, q_gnd_avg )
print "The location of the ground marker frame within mocap coordinates (units are mm):\n", ground

# ==================================================================
# Generate a homogeneous transform representing the robot marker in mocap coordinates.
# This assumes the marker didn't move and just averages over all components.  
# Convert from the mocap default meter coordinates to millimeters
# for consistency with the ABB robot.

t_robot, x_robot, q_robot, ypr_robot = data.trajectory('Robot')
x_rob_avg = 1000 * np.mean( x_robot, axis=0 )
q_rob_avg = xyzw_to_wxyz( quat.normalize(np.mean( q_robot, axis=0 )))

robot_mc = make_threexform_from_pos_quat( x_rob_avg, q_rob_avg )
print "The location of the robot marker frame in mocap coordinates:\n", robot_mc

# For this trial, the robot TCP was positioned to: [1000, 1000, 2000], [0.706,
# 0.000, 0.000, 0.708], expressed in the base coordinates.  Note that the track
# axis position was not recorded, so an arbitrary X offset has been added to
# place the robot in the approximate position.

robot_tcp = np.dot( xform.translation( 1000.0 + 2500, 1000.0, 2000.0 ), 
                    quat.to_threexform( np.array( ( math.sqrt(2)/2, 0.000, 0.000, math.sqrt(2)/2))))

print "The location of the robot TCP in world coordinates:\n", robot_tcp

# The mocap system assigned coordinates to the robot marker frame which were
# aligned with the mocap system.  The following transform expresses the motion
# capture view of the robot marker frame in world coordinates.
robot_marker_frame = np.dot( robot_tcp, xform.yaw_pitch_roll( 180.0, 0.0, 90.0 ) )

print "The location of the robot marker frame in world coordinates:\n", robot_marker_frame

# The motion capture coordinates within the world frame can be computed now, since the robot marker frame has been located within each system.
#   robot_marker_frame : world coords -> robot markers
#   robot_mc           : mocap coords -> robot markers
# 
# What we want is : world coords -> mocap coords
mocap_coords = np.dot( robot_marker_frame, np.linalg.inv( robot_mc ))

print "Motion capture coordinates within world frame:\n", mocap_coords

# ==================================================================
# Compute the tool trajectory as expressed in the world frame. 
tool_traj_world = [np.dot( mocap_coords, ti) for ti in tool_traj]

# For testing, generate a plot file with the origin and points
# representing the ends of the unit vectors for each tool point.
if gen_debug_files: 
    print "Generating tool data plot file."
    datafiles.write_trajectory_plot_file( "plots/tool.dat", times, tool_traj_world)

# ==================================================================
print "Generating tool data file."
datafiles.write_frame_trajectory_file( os.path.join( data_folder_name, base_name + ".traj"), times, tool_traj_world )

