"""dfab/debug/rhinoscriptsyntax.py

Copyright (c) 2014, Garth Zeglin.  All rights reserved. Licensed under the terms
of the BSD 3-clause license as included in LICENSE.

This is a trivial emulation of the rhinoscriptsyntax module provided by Rhino to
allow debugging of other code in a non-Rhino interpreter.  Only a tiny subset of
the module is supported.

This uses numpy and is thus unlikely to actually work in Rhino.

Each Rhino Plane is represented as a homogeneous transform in a 4x4 ndarray.
"""
import math
import numpy as np

def PlaneFromFrame( origin, xaxis, yaxis ):
    """Create a homogeneous transform from a origin vector, and X and Y basis vectors.
    
    All arguments are three-element sequences, and the output is a 4x4 numpy ndarray.
    """
    
    # normalize basis and compute a Z unit vector
    x = np.array(xaxis)  # make sure these are in numpy types
    y = np.array(yaxis)
    x = x * (1.0 / math.sqrt(np.dot(x, x)))
    y = y * (1.0 / math.sqrt(np.dot(y, y)))
    z = np.cross( x, y )

    # extend each vector to 4 elements and assemble a transform matrix
    return np.vstack((np.hstack((x, 0)), np.hstack((y, 0)), np.hstack((z, 0)), np.hstack((origin, 1)))).transpose()
