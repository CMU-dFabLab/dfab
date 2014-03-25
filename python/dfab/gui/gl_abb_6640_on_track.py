"""Render an OpenGL cartoon of an ABB 6640 arm on a track using plain OpenGL and GLU.

gl_abb_6640_on_track.py, Copyright (c) 2001-2014 Garth Zeglin. All rights
reserved. Licensed under the terms of the BSD 3-clause license as included in
LICENSE.
"""

# All links drawn to scale in metric units.  One world coordinate
# unit is a one meter in real space.

import math

from OpenGL.GL import *
from OpenGL.GLU import *

from gl_drawing import *

from dfab.ABB6640.parameters import *

def RADIAN(degrees):   return degrees * math.pi / 180.0
def DEG(radians):      return radians * 180.0 / math.pi

# shared quadric object, only valid while drawing
quadric = None

#================================================================
# Dimensional constants. Most are taken from ABB document 3HAC028284-001 Ref F page 13.

# A number of exact kinematic parameters are imported from
# dfab.ABB6640.parameters. The following parameters are only used to define
# graphical features and are a coarse approximation.
track_length  =  6.900  # number from Josh Bard
track_height   = 0.290
mount_radius   = 0.380
mount_height   = 0.200
base_radius    = 0.450
elbow_length   = 0.700
forearm_length = 0.700
forearm_radius = 0.100
flange_radius  = 0.080

#================================================================
# Component colors.
track_color  = [ 0.90, 0.50, 0.20 ]
link_color   = [ 0.70, 0.50, 0.20 ]
joint_color  = [ 0.35, 0.25, 0.10 ]

#================================================================
# Draw a representation of a joint.  The coordinate system is
# assumed to lie along the world axes with Z up, X forward, Y to
# the left.

# This draws a closed cylinder with an axis along Y, centered on
# the current origin.

def draw_joint( radius, length ):
    glPushMatrix()
    glRotatef( -90.0, 1.0, 0.0, 0.0 )        # rotate the +Z axis to point along -Y
    glTranslatef( 0.0, 0.0, -0.5*length )    # translate along local -Z
    glColor3fv( joint_color )

    # orient the gluDisk normals to close the cylinder properly
    gluQuadricOrientation( quadric, GLU_INSIDE )
    gluDisk( quadric, 0.0, radius, 8, 1 )
    gluQuadricOrientation( quadric, GLU_OUTSIDE )

    gluCylinder( quadric, radius, radius, length, 8, 1)
    glTranslatef( 0.0, 0.0, length )
    gluDisk( quadric, 0.0, radius, 8, 1 )

    glPopMatrix()

#================================================================

def gl_abb_6640_on_track_draw( tool_ctm, track, a1, a2, a3, a4, a5, a6 ):
    # make a temporary quadric to share
    global quadric
    quadric = gluNewQuadric()
    gluQuadricNormals( quadric, GLU_SMOOTH )
    gluQuadricDrawStyle( quadric, GLU_FILL )  # shaded opaque surfaces
    # gluQuadricDrawStyle( quadric, GLU_LINE )  # wireframe for debugging

    glPushMatrix() # start of the arm

    # Draw the stationary track.  The track is drawn a little longer than the
    # logical length so that the base can remain over it.
    glColor3fv( track_color )
    glPushMatrix()
    glTranslatef( 0.5 * track_length, 0.0, 0.5 * track_height )
    gl_draw_box( track_length + 1.0, 1.0, track_height )
    glPopMatrix()

    glTranslatef( track, 0.0, track_z_offset )       # track translation along X, vertical offset along Z

    # Draw a cylindrical representation of the irregular base shape.
    glColor3fv( link_color )
    glPushMatrix()
    gluCylinder( quadric, mount_radius, mount_radius, mount_height, 15, 1 )
    glTranslatef( 0.0, 0.0, mount_height )
    gluDisk( quadric, 0.0, mount_radius, 15, 1 )
    glPopMatrix()

    # First axis in base.
    glRotatef( DEG(a1), 0.0, 0.0, 1.0 )  # axis 1 rotation around Z

    # Draw a cylindrical representation of the upper part of the base.
    glPushMatrix()
    glColor3fv( link_color )
    glTranslatef( 0.0, 0.0, mount_height + 0.05 )
    gluCylinder( quadric, base_radius, base_radius, 0.400, 15, 1 )
    glTranslatef( 0.0, 0.0, 0.400 )
    gluDisk( quadric, 0.0, base_radius, 15, 1 )
    glPopMatrix()

    # Second axis in base.
    glTranslatef( axis_2_x, 0.000, axis_2_z) # axis 2 forward of origin and above top of track
    glRotatef( DEG(a2), 0.0, 1.0, 0.0 )      # axis 2 rotation around Y

    # Cylindrical approximation of the Axis 2 joint.
    draw_joint( 0.150, 0.820 )

    # Cylindrical approximation of major vertical link up to axis 3.
    glColor3fv( link_color )
    gluCylinder( quadric, 0.15, 0.15, axis_3_z, 10, 1 )   # these numbers are guesses

    # Axis 3 is directly above axis 2.
    glTranslatef( 0.000, 0.000, axis_3_z ) # axis 3 above axis 2
    glRotatef( DEG(a3), 0.0, 1.0, 0.0 )    # axis 3 rotation around Y

    # Cylinder to represent axis 3.
    draw_joint( 0.1, 0.400 )

    # There is a vertical offset from axis three to the horizontal link axis.
    glTranslatef( 0.0, 0.0, wrist_z)

    # Conical approximation of the "elbow", the base of the horizontal link, which is oriented along +X.
    glPushMatrix()
    glTranslatef( -0.250, 0.0, 0.0 )
    glRotatef( 90, 0.0, 1.0, 0.0)   # rotate +Z down along +X
    glColor3fv( link_color )
    gluQuadricOrientation( quadric, GLU_INSIDE )
    gluDisk( quadric, 0.000, 0.200, 10, 1 )
    gluQuadricOrientation( quadric, GLU_OUTSIDE )
    gluCylinder( quadric, 0.200, forearm_radius, elbow_length, 10, 1 )
    glPopMatrix()

    # Move to the wrist joint center, which is forward of Axis 3 along X.  (It is
    # also above Axis 3, already incorporated.)
    glTranslatef( wrist_x, 0.0, 0.0 )

    # Apply the first wrist joint, which is physically incorporated
    # into the horizontal link.
    glRotatef( DEG(a4), 1.0, 0.0, 0.0 )   # rotation around +X

    # Cylindrical approximation of the second part of the horizontal link.
    glPushMatrix()
    glTranslatef( -forearm_length, 0.0, 0.0)
    glRotatef( 90, 0.0, 1.0, 0.0)   # rotate +Z down along +X
    glColor3fv( link_color )
    gluCylinder( quadric, forearm_radius, forearm_radius, forearm_length, 10, 1 )
    glPopMatrix()

    # Apply the second wrist joint around Y, and draw a representation
    # of the joint.  The moving part is actually mostly internal and
    # not very visible, but the outer part isn't drawn.  This
    # appoximates the inner part.
    glRotatef( DEG(a5), 0.0, 1.0, 0.0 )  # axis 5 rotation around Y
    draw_joint( 0.100, 0.200 )

    # Apply the final wrist rotation around X.
    glRotatef( DEG(a6), 1.0, 0.0, 0.0 )  # axis 6 rotation around X

    # Cylindrical approximation ofthe mounting link.
    glPushMatrix()
    glRotatef( 90, 0.0, 1.0, 0.0)   # rotate +Z down along +X
    glColor3fv( link_color )
    gluCylinder( quadric, flange_radius, flange_radius, endplate_x, 10, 1 )
    glTranslatef( 0.0, 0.0, endplate_x )
    gluDisk( quadric, 0.0, flange_radius, 10, 1 )
    glPopMatrix()

    glPopMatrix()                # end of the arm

    gluDeleteQuadric( quadric )  # free the temporary quadric
    quadric = None
    return
    
#================================================================
def gl_abb_6640_on_track_transform( track, a1, a2, a3, a4, a5, a6):
    glTranslatef( track, 0.0, track_z_offset )       # track translation along X, vertical offset along Z
    glRotatef( DEG(a1), 0.0, 0.0, 1.0 )  	    # axis 1 rotation around Z
    glTranslatef( axis_2_x, 0.000, axis_2_z)  	    # axis 2 forward of origin and above top of track
    glRotatef( DEG(a2), 0.0, 1.0, 0.0 )  	    # axis 2 rotation around Y
    glTranslatef( 0.000, 0.000, axis_3_z )  	    # axis 3 above axis 2
    glRotatef( DEG(a3), 0.0, 1.0, 0.0 )  	    # axis 3 rotation around Y
    glTranslatef( wrist_x, 0.000, wrist_z )  	    # wrist center above and in front of axis 2
    glRotatef( DEG(a4), 1.0, 0.0, 0.0 )  	    # axis 4 rotation around X
    glRotatef( DEG(a5), 0.0, 1.0, 0.0 )  	    # axis 5 rotation around Y
    glRotatef( DEG(a6), 1.0, 0.0, 0.0 )  	    # axis 6 rotation around X
    glRotatef( 90, 0.0, 1.0, 0.0)        	    # rotate +Z down along +X
    glTranslatef( 0.000, 0.000, endplate_x )  	    # flange in front of wrist center
    return

#================================================================
