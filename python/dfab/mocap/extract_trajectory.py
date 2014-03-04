"""Process a Optitrack motion capture .csv file into a world-frame trajectory.

Copyright (c) 2014, Garth Zeglin.  All rights reserved. Licensed under the terms
of the BSD 3-clause license as included in LICENSE.

This is the back end processor shared by the command line programs and the graphical shell.
"""

import os
import math
import argparse
import json
import traceback
import numpy as np
import dfab.mocap.optitrack_csv as optitrack
import dfab.mocap.datafiles as datafiles
import dfab.geometry.quaternion as quat
import dfab.geometry.threexform as xform
import dfab.geometry

# use a more readable numpy output format
np.set_printoptions(suppress=True, precision=8)

# ==================================================================
def load_csv_data( filename, verbose = False ):
    if verbose: print "Loading", filename
    data = optitrack.Run().ReadFile( data_dir = ".", filename = filename, verbose = False )
    if verbose: print "Found %d rigid bodies, %d frames." % (data.trackablecount, data.framecount )
    if verbose: print "Bodies:",[body.name for body in data.trackables]
    return data

# ==================================================================
def extract_trajectory( data, subsampling_ratio = 12, body = 'Tool', verbose = False ):
    """Transform a sequence of mocap body frames into a world-frame trajectory.

    The position data is converted from meters to millimeters.

    Optional arguments:
    subsampling_ratio -- the ratio of frames to frames processed, default is 12 for 10Hz samples
    body -- the name of the desired body in the mocap dataset
    verbose -- true for more console output
    """

    # Extract three lists of vectors defining the tool motion:
    # timestamps, positions, and orientation quaternions.
    times, x_tool, q_tool, ypr_tool = data.trajectory( body )

    # use a Python slice with a step index to subsample the input.
    times     = times[::subsampling_ratio]
    x_tool    = x_tool[::subsampling_ratio]
    q_tool    = q_tool[::subsampling_ratio]
    ypr_tool  = ypr_tool[::subsampling_ratio]

    # Convert from the mocap default meter coordinates to millimeters
    # for consistency with the ABB robot.
    x_tool *= 1000

    # Convert the (x, y, z, w) quaternions returned by the mocap system to (w,x,y,z)
    # order as used by the quaternion code.
    q_tool = dfab.geometry.xyzw_to_wxyz(q_tool)

    if verbose: print "Found %d samples for body %s." % (len(times), body )
    return times, x_tool, q_tool, ypr_tool

#================================================================
def process_trajectory( args ):
    """Process a CSV file into a trajectory file."""

    # Read the parameter file and retrieve the mocap calibration matrix.
    try:
        input_params = dfab.mocap.datafiles.read_parameter_file( args.param )
        mocap_to_world = np.array( input_params['mocap_to_world'] )
    except:
        print "Unable to load parameter file: " + str(traceback.format_exc()) + \
            "\nThe script was unable to load the parameter file.  The parameter file " + \
            "is the output file from estimate_mocap_calibration which defines the " + \
            "relationship between the motion capture coordinates and robot coordinates."
        raise

    # Extract a single trajectory from the CSV file in mocap coordinates.
    try:
        data = load_csv_data( args.csv, verbose = args.verbose )
    except:
        print "Unable to load CSV file: " + str(traceback.format_exc()) + \
            "\nThe script was unable to load the Optitrack CSV file.  The CSV " +\
            "is the complete motion capture data saved from the Optitrack Motive software."
        raise

    try:
        times, x_tool, q_tool, ypr_tool = extract_trajectory( data, subsampling_ratio = args.rate, body = args.body, verbose = args.verbose )
    except:
        print "Unable to extract trajectory: " + str(traceback.format_exc()) + \
            "\nThe script was unable to extract body " + args.body + " from the Optitrack CSV file."
        raise


    # Generate a homogeneous transform representing each tool frame.
    tool_traj = [ dfab.geometry.pos_quat_to_threexform( position, orientation ) for (position, orientation) in zip( x_tool, q_tool) ]
    
    # Compute the tool trajectory as expressed in the world frame. 
    if args.verbose: print "Applying mocap calibration matrix:\n", mocap_to_world
    tool_traj_world = [np.dot( mocap_to_world, ti) for ti in tool_traj]

    # ==================================================================
    if args.output is not None:
        if args.verbose: print "Generating trajectory file", args.output
        datafiles.write_frame_trajectory_file( args.output, times, tool_traj_world )
    else:
        print "Trajectory:"
        for m in tool_traj_world: print m

#================================================================
