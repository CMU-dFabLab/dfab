"""Basic drawing functions that only depend on plain OpenGL.  These are higher
level than raw GL and similar in purpose to the GLU functions.

gl_drawing.py, Copyright (c) 2001-2014, Garth Zeglin. All rights
reserved. Licensed under the terms of the BSD 3-clause license as included in
LICENSE.
"""

from OpenGL.GL import *
from OpenGL.GLU import *
import math

def RADIAN(degrees):   return degrees * math.pi / 180.0
def DEG(radians):      return radians * 180.0 / math.pi

#================================================================
def gl_draw_checkerboard_ground_plane( xmin = -3.0, ymin = -3.0, xmax = 3.0, ymax = 3.0, fore = 0.8, back = 0.2, gnd_z = 0.0 ):
    """Draw a ground plane as white and gray unit squares within a rectangle."""
    glBegin( GL_QUADS )
    x0 = math.floor(xmin)
    y0 = math.floor(ymin)
    xcount = int(math.ceil(xmax - xmin))
    ycount = int(math.ceil(ymax - ymin))

    for i in range(xcount):
        x = x0 + i
        for j in range(ycount):
            y = y0 + j
            intensity = fore if ((i&1)^(j&1)) == 0 else back
            glColor3f( intensity, intensity, intensity )
            glNormal3f(0.0, 0.0, 1.0)
            glVertex3f( x      , y      , gnd_z )
            glVertex3f( x + 1.0, y      , gnd_z )
            glVertex3f( x + 1.0, y + 1.0, gnd_z )
            glVertex3f( x      , y + 1.0, gnd_z )
    glEnd()
    return

#================================================================
def gl_init_default_lighting():
    """Define some kind of basic OpenGL lighting so things are visible."""

    # With W==0, specify the light as directional and located at these
    # coordinates in the current modelview.  With a directional light,
    # diffuse and specular components will take direction into account
    # but not position, so this produces a "solar" field of parallel
    # uniform rays.
    light_position = [ 5.0, -5.0, 5.0, 0.0 ]

    # With W==1, specify the light as positional and located at these
    # coordinates in the current modelview.
    # light_position = [ 5.0, -5.0, 5.0, 1.0 ]

    light_specular = [ 1.0, 1.0, 1.0, 1.0 ]   # specular RGBA intensity
    light_ambient  = [ 0.1, 0.1, 0.1, 1.0 ]   # ambient RGBA intensity
    light_diffuse  = [ 0.9, 0.9, 0.9, 1.0 ]   # diffuse RGBA intensity

    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)

    # The attenuation for positional lights (not directional) is
    # defined by distance D between a vertex and a light as follows:
    #   factor = 1.0 / ( constant + D*linear + D*D*quadratic ).
    #  The default parameters are (constant == 1, linear == 0, quadratic == 0).
    # glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.1 )

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glDepthFunc(GL_LEQUAL)
    glEnable(GL_DEPTH_TEST)

    # Set the default material specularity.
    glMaterialf(GL_FRONT, GL_SHININESS, 5.0 )
    specularity = [ 0.3, 0.3, 0.3, 1.0 ]
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularity)

    # By default, have material parameters track the current color, so
    # the material color will can be changed just by calls to glColor.
    # The default glColorMaterial mode is GL_FRONT_AND_BACK and
    # GL_AMBIENT_AND_DIFFUSE.
    glEnable(GL_COLOR_MATERIAL)

    return
#================================================================
def set_camera_xyzypr( x, y, z,             # camera position
                       yaw, pitch, roll,    # camera orientation
                       fov,                 # field of view
                       far ):               # view distance
    """Set the view using general camera parameters.  The camera has a
    location in space, an orientation specified as a quaternion, a
    field of view specified in degrees, and a camera view range
    (clipping depth).

    Arguments:

    x, y, z            -- camera position
    yaw, pitch, roll   -- camera orientation
    fov                -- field of view in degrees
    far                -- view distance
    """

    view_x, view_y, winWidth, winHeight = glGetIntegerv(GL_VIEWPORT)

    if winWidth < winHeight:
        hwidth  = math.tan(0.5 * RADIAN(fov));
        hheight = hwidth * (float(winHeight) / winWidth)
    else:
        hheight = math.tan(0.5 * RADIAN(fov))
        hwidth  = hheight * (float(winWidth) / winHeight)

    # set projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum( -hwidth, hwidth, -hheight, hheight, 1.0, far )

    # set camera transform
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity() # start as right handed system looking along -Z

    # rotate to look along +X with +Z up
    glRotatef( 90.0, 0.0, 0.0, 1.0 )
    glRotatef( 90.0, 0.0, 1.0, 0.0 )

    # position the focal plane
    glRotatef(DEG (roll), -1.0,  0.0,  0.0)
    glRotatef(DEG (pitch), 0.0, -1.0,  0.0)
    glRotatef(DEG (yaw),   0.0,  0.0, -1.0)
    glTranslatef( -x, -y, -z )

    return

#================================================================
# FIXME: This is translated from C and could probably be made faster for Python.

# 24x3 vertex data for a rectangular solid.
cube = \
  [
    [-1,-1, 1],    [ 1,-1, 1],    [ 1, 1, 1],    [-1, 1, 1],        # top    (Z ==  1)
    [-1,-1,-1],    [-1, 1,-1],    [ 1, 1,-1],    [ 1,-1,-1],        # bottom (Z == -1)
    [-1, 1, 1],    [ 1, 1, 1],    [ 1, 1,-1],    [-1, 1,-1],        # left   (Y ==  1)
    [-1,-1, 1],    [-1,-1,-1],    [ 1,-1,-1],    [ 1,-1, 1],        # right  (Y == -1)
    [ 1,-1,-1],    [ 1, 1,-1],    [ 1, 1, 1],    [ 1,-1, 1],        # front  (X ==  1)
    [-1,-1,-1],    [-1,-1, 1],    [-1, 1, 1],    [-1, 1,-1] ]       # back   (X == -1)

# 6x3 list for normal vectors
cubenormal = \
  [
    [  0.0,  0.0,  1.0 ],         # top
    [  0.0,  0.0, -1.0 ],         # bottom
    [  0.0,  1.0,  0.0 ],         # left
    [  0.0, -1.0,  0.0 ],         # right
    [  1.0,  0.0,  0.0 ],         # front
    [ -1.0,  0.0,  0.0 ]]         # back


def gl_draw_box( x, y, z ):
    """Draw a simple box centered on the origin.
    Arguments:
    x, y, z -- dimensions along the axes
    """
    hx = 0.5*x;
    hy = 0.5*y;
    hz = 0.5*z;

    glBegin (GL_QUADS)

    i = 0
    for face in range(6):
        glNormal3fv ( cubenormal[face] )
        for j in range(4):
            glVertex3f ( hx if (cube[i][0] > 0) else -hx,
                         hy if (cube[i][1] > 0) else -hy,
                         hz if (cube[i][2] > 0) else -hz )
            i += 1
    glEnd()
    return

#================================================================
def gl_draw_arrow( length, quad ):
    """Draw an arrow along +Z in OpenGL using a line and a GLU cone (i.e. tapered cylinder).

    Arguments:
    length -- the length of each axis
    quadric -- a GLU quadric object to use for drawing
    """

    # draw the stem
    glBegin( GL_LINES )
    glVertex3f( 0.0, 0.0, 0.0 )
    glVertex3f( 0.0, 0.0, 0.75*length )
    glEnd()

    # draw the conical tip
    glPushMatrix()
    glTranslatef( 0.0, 0.0, 0.75*length )
    gluCylinder( quad, 0.1*length, 0.0, 0.25*length, 9, 1 )
    glPopMatrix()
    return

def gl_draw_frame(  length = 1.0, quadric = None):
    """Illustrate the current OpenGL transformation matrix with red, green, and blue arrows aligned with the unit axes.

    Optional arguments:
    length -- the length of each axis (default = 1.0 unit)
    quadric -- a GLU quadric object to use for drawing (default is to create a temporary one)
    """

    # create a new quadric state if none was provided
    quad = gluNewQuadric() if quadric is None else quadric

    glColor3f( 1.0, 0.0, 0.0 )
    glPushMatrix()
    glRotatef( 90.0, 0.0, 1.0, 0.0 )
    gl_draw_arrow( length, quad ) # +X

    glRotatef( -90.0, 1.0, 0.0, 0.0 )
    glColor3f( 0.0, 1.0, 0.0 )
    gl_draw_arrow( length, quad ) # +Y

    glPopMatrix()
    glColor3f( 0.0, 0.0, 1.0 )
    gl_draw_arrow( length, quad ) # +Z

    if quadric is None:
        gluDeleteQuadric( quad )  # free the temporary quadric

    return

def gl_draw_transform( matrix, **kwargs ):
    """Draw a red-green-blue X-Y-Z coordinate frame representing the given homogeneous transform matrix."""

    glPushMatrix()
    glMultMatrixd( matrix.transpose() ) # OpenGL expects a different matrix layout
    gl_draw_frame( **kwargs )
    glPopMatrix()

#================================================================
