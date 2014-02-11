"""Data file utilities for dFab motion capture package.

Copyright (c) 2014, Garth Zeglin.  All rights reserved. Licensed under the terms
of the BSD 3-clause license as included in LICENSE.

This module produces and parses data files in several ad hoc plain text formats
convenient for readability and portability.

This deliberately *does not* import numpy, as it is intended to work with either
Rhino IronPython, 32-bit IronPython, or 32-or-64-bit CPython.

"""

################################################################
def write_point_trajectory_file( filename, times, points ):
    """Write a plain ASCII data matrix for plotting a trajectory of moving points.

    The units are assumed to be millimeters (and noted in the file comments).

    filename -- the full path to the output file to create
    times    -- N-element list of timestamps, one per frame
    points   -- N-element list of vectors with 3 or more elements (first three used)
    """

    plot = open( filename, "w")
    plot.write("""# point trajectory file 
# Each line represents one Cartesian points for plotting the moving point, e.g.
# the origin of a moving coordinate frame.
# format: timestamp x, y, z
# units: seconds, millimeters
""")

    for i,pt in enumerate( points ):
        plot.write( "%f  " % times[i] )
        plot.write( "%f %f %f\n" % tuple( pt[0:3] ) )
    plot.close()
    return

################################################################
def write_trajectory_plot_file( filename, times, frames ):
    """Write a plain ASCII data matrix for plotting a trajectory of moving frames expressed as homogeneous transforms.

    The units are assumed to be millimeters (and noted in the file comments).

    filename -- the full path to the output file to create
    times    -- N-element list of timestamps, one per frame
    frames   -- N-element list of 4x4 homeogeneous transform matrices
    """

    plot = open( filename, "w")
    plot.write("""# frame plot file 
# Each line represents four Cartesian points for plotting the origin and axis
# vectors of a moving coordinate frame.  A <> in the format represents an (x,y,z)
# triple.  Each axis vector has magnitude 20mm for visibility.
# format: timestamp <origin> <end of X axis> <end of Y axis> <end of Z axis>
# units: seconds, millimeters
""")

    for i,tool in enumerate( frames ):
        origin = tool[0:3,3] # origin vector, expressed in ground frame
        xaxis  = tool[0:3,0]
        yaxis  = tool[0:3,1]
        zaxis  = tool[0:3,2]
        plot.write( "%f   " % times[i] )
        plot.write( "%f %f %f   " % tuple(origin) )
        plot.write( "%f %f %f   " % tuple(origin+20*xaxis) )
        plot.write( "%f %f %f   " % tuple(origin+20*yaxis) )
        plot.write( "%f %f %f\n" % tuple( origin+20*zaxis) )
    plot.close()
    return

################################################################
def write_frame_trajectory_file( filename, times, frames ):
    """Write a plain ASCII data matrix for a trajectory of moving frames expressed as homogeneous transforms.

    The units are assumed to be millimeters (and noted in the file comments).

    filename -- the full path to the output file to create
    times    -- N-element list of timestamps, one per frame
    frames   -- N-element list of 4x4 homeogeneous transform matrices
    """

    plot = open( filename, "w")
    plot.write("""# frame trajectory file 
# Each line represents the origin and axis vectors of a moving coordinate frame.
# A <> in the format represents an (x,y,z) triple.
# format: timestamp <origin> <X axis> <Y axis> <Z axis>
# units: seconds, millimeters
""")

    for i,tool in enumerate( frames ):
        xaxis  = tool[0:3,0]   # unit X axis basis vector
        yaxis  = tool[0:3,1]   # unit Y axis basis vector
        zaxis  = tool[0:3,2]   # unit Z axis basis vector
        origin = tool[0:3,3]   # origin vector, expressed in ground frame
        plot.write( "%f   " % times[i] )
        plot.write( "%f %f %f   " % tuple(origin) )
        plot.write( "%f %f %f   " % tuple(xaxis) )
        plot.write( "%f %f %f   " % tuple(yaxis) )
        plot.write( "%f %f %f\n"  % tuple( zaxis) )
    plot.close()
    return

################################################################
def read_frame_trajectory_file( filename ):
    """Read a plain ASCII frame trajectory file specifying a sequence of coordinate frames.

    Returns path, timestamps:
    
    path --- 3-dim list representing a list of coordinate frames : [ frame0, frame1...]
    timestamps --- list of scalars [ time0, time1, ...]

    Each frame is a 2-dim list in the following form:
    frame: [[ origin_x, origin_y, origin_z,],   origin vector of frame in parent frame
            [ unitx_x,  unitx_y,  unitx_z, ],   unit basis X vector expressed in parent frame
            [ unity_x,  unity_y,  unity_z, ],   unit basis Y vector expressed in parent frame
            [ unitz_x,  unitz_y,  unitz_z, ]]   unit basis Z vector expressed in parent frame
    """
    file = open(filename, "r")

    timestamps = list()
    path = list()

    for line in file:
        # eliminate leading spaces
        line = line.strip()

        # ignore comments and empty lines
        if len(line) == 0 or line[0] == '#':
            continue

        # divide on whitespace and convert to numbers
        nums = [float(x) for x in line.split()]
        
        # separate out components and build lists

        timestamps.append( nums[0] )

        origin = list( nums[1:4] )
        unitx  = list( nums[4:7] )
        unity  = list( nums[7:10] )
        unitz  = list( nums[10:13] )

        path.append( list( (origin, unitx, unity, unitz ) ) )

    return path, timestamps

################################################################
