"""  Example code for generating a Rhino 'plane' (e.g. coordinate frame) from an origin and XY basis vectors.

Inputs visible in Grasshopper:
  (none)

Outputs visible in Grasshopper:
  out
  a    
"""

import rhinoscriptsyntax as rs

# syntax of the PlaneFromFrame operator:
# rs.PlaneFromFrame (origin, x_axis, y_axis)

origin = (100, 200, 300)
xaxis  = (1,0,0)
yaxis  = (0,0,1)
plane  = rs.PlaneFromFrame( origin, xaxis, yaxis ) 
a = plane
