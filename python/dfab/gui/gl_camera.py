"""Interactive controls for a 3D virtual camera using mouse input and modifier
keys.  The actual view transformations are handled by gl_drawing.  This is not
specific to any GUI toolkit, the user passes in generic representations of user
input.

gl_camera.py, Copyright (c) 2001-2014, Garth Zeglin. All rights
reserved. Licensed under the terms of the BSD 3-clause license as included in
LICENSE.

The default motion is object-centric: the camera moves at a constant radius
around a fixation point as the mouse motions reorient the view.

"""

import math
import gl_drawing

def radians(degrees):
    return degrees * math.pi / 180.0

class camera:
    # additional parameters which could be made variables if needed
    minimum_fixation_distance = 2.0
    maximum_field_of_view     = 40.0
    minimum_field_of_view     =  2.0

    # camera position
    cam_x = 0.0
    cam_y = 0.0
    cam_z = 0.0

    # camera orientation and field of view
    cam_pan   = radians( 160.0 )
    cam_tilt  = radians( 15.0 )
    cam_fov   = 40.0

    # fixation point
    fix_x     = 1.0
    fix_y     = 0.0
    fix_z     = 0.9

    # distance the camera stays from the fixation point
    fix_distance = 3.0

    # previous mouse point
    last_drag_x = 0
    last_drag_y = 0
    dragging = False # true if drag is active

    # toolkit-neutral values for input event state
    left_button = False
    right_button = False
    shift_modifier = False
    control_modifier = False
    alt_modifier = False


    # update the camera center given the angles around the fixation point
    def recomputeCameraPositionForFixation( self ):
        self.cam_z = self.fix_z + ( self.fix_distance * math.sin( self.cam_tilt))
        self.cam_x = self.fix_x + (-self.fix_distance * math.cos( self.cam_tilt) * math.cos( self.cam_pan ))
        self.cam_y = self.fix_y + (-self.fix_distance * math.cos( self.cam_tilt) * math.sin( self.cam_pan ))
        
    def __init__(self):
        self.recomputeCameraPositionForFixation()
        return

    def set_view_angle( self, pan, tilt ):
        self.cam_pan = pan
        self.cam_tilt = tilt
        self.recomputeCameraPositionForFixation()
        return

    def set_fixation( self, x, y, z ):
        """Set the fixation point of the camera, keeping the pan, tilt, and viewing
        radius constant.  The camera translates along the same vector as the
        change of fixation.
        """

        self.fix_x = x
        self.fix_y = y
        self.fix_z = z
        self.recomputeCameraPositionForFixation()
        return

    def set_location( self, x, y, z ):
        """Set the location of the camera, keeping the fixation point constant and
        updating the pan, tilt, and radius of the camera locus around the
        fixation point.
        """

        self.cam_x = x
        self.cam_y = y
        self.cam_z = z
        self.cam_pan  = math.atan2( self.fix_y - self.cam_y, self.fix_x - self.cam_x )
        self.fix_distance = math.sqrt( math.pow(self.cam_x - self.fix_x, 2) + math.pow(self.cam_y - self.fix_y, 2) + math.pow(self.cam_z - self.fix_z, 2))
        xy_distance = math.sqrt( math.pow(self.cam_x - self.fix_x, 2) + math.pow(self.cam_y - self.fix_y, 2))
        self.cam_tilt = math.atan2( self.cam_z - self.fix_z, xy_distance )

        self.recomputeCameraPositionForFixation()
        return

    def set_current_transform( self ):
        """Set the OpenGL projection and modelview transforms to render the view from the camera."""
        gl_drawing.set_camera_xyzypr( self.cam_x, self.cam_y, self.cam_z, self.cam_pan, self.cam_tilt, 0.0, self.cam_fov, 100.0 )
        return

    # Process mouse down to initialize a change of camera view drag operation.
    def mouse_down( self, x, y, left = False, right = False, shift = False, control = False, alt = False ):
        self.left_button = left
        self.right_button = right
        self.shift_modifier = shift
        self.control_modifier = control
        self.alt_modifier = alt

        if self.left_button:
            self.last_drag_x = x
            self.last_drag_y = y
            self.dragging = True
        else:
            self.dragging = False

        return

    # Process mouse drag inputs to spin the camera around a fixation point.  This
    # method is appropriate for viewing a fixed scene.
    def mouse_drag_around_fixation( self, x, y ):
        if self.dragging:
            # positive X: right, positive Y: down
            xdiff = x - self.last_drag_x;
            ydiff = self.last_drag_y - y;  # normalize 
            self.last_drag_x = x;
            self.last_drag_y = y;

            if self.shift_modifier:
                # Control the magnification of the view.  Zooming closer occurs in two
                # phases: first, adjust the distance from the camera to the focal point,
                # which will adjust the apparent magnification without changing the
                # perspective.  Then to avoid clipping by getting too close, continue to
                # zoom by reducing the field of view.  The process is reversed for
                # zooming out.

                if ydiff > 0 : # zooming in
                    if self.fix_distance > self.minimum_fixation_distance:
                        self.fix_distance -= 0.1 * ydiff;
                    else:
                        self.cam_fov -= 1.0 * ydiff;
                        if self.cam_fov < self.minimum_field_of_view: self.cam_fov = self.minimum_field_of_view;
                else: # zooming out
                    if self.cam_fov < self.maximum_field_of_view:
                        self.cam_fov += -1.0 * ydiff
                    else:
                        self.fix_distance += -0.1 * ydiff

            elif self.control_modifier:
                # Move the fixation point relative to the current camera
                # position.  First compute the camera image plane basis
                # vectors, then use them to project the drag vector into the
                # world.  This may not be exactly right, but it is close
                # enough to use for a control.
                camera_right_x = math.cos(self.cam_tilt) * math.sin(self.cam_pan)
                camera_right_y = math.cos(self.cam_tilt) * (-math.cos(self.cam_pan))
                camera_right_z = math.sin(self.cam_tilt)
                camera_up_x    = math.sin(self.cam_tilt) * math.cos(self.cam_pan)
                camera_up_y    = math.sin(self.cam_tilt) * math.sin(self.cam_pan)
                camera_up_z    = math.cos(self.cam_tilt)

                # rotate the drag increment from the camera frame to the world frame
                self.fix_x -= 0.01 * ((xdiff * camera_right_x) + (ydiff * camera_up_x));
                self.fix_y -= 0.01 * ((xdiff * camera_right_y) + (ydiff * camera_up_y));
                self.fix_z -= 0.01 * ((xdiff * camera_right_z) + (ydiff * camera_up_z));

            else:
                # Adjust pan and tilt without changing fixation; the camera
                # will whirl around the focal point.

                self.cam_pan  += -0.01 * xdiff
                self.cam_tilt += -0.01 * ydiff

            self.recomputeCameraPositionForFixation()
    
