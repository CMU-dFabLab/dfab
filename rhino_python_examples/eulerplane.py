"""Example code for generating a Rhino 'plane' (e.g. coordinate frame) from Euler angle rotations. 

authors: Joshua Bard <jdbard@cmu.edu>

 Inputs visible in Grasshopper:
  x
  y
  z
  rx
  ry
  rz

 Outputs visible in Grasshopper:
  out
  a
  xAxis
  yAxis
  zAxis
"""

import rhinoscriptsyntax as rs
 
basePlane = rs.WorldXYPlane()
movePoint = rs.AddPoint(x,y,z)
movePlane = rs.MovePlane(basePlane,movePoint)
 
rzPlane = rs.RotatePlane(movePlane,rz,basePlane.ZAxis)
rxPlane = rs.RotatePlane(rzPlane,rx,rzPlane.XAxis)
rotatePlane = rs.RotatePlane(rxPlane,ry,rxPlane.YAxis)
 
a = rotatePlane
 
red = 255,0,0
green = 0,255,0
blue = 0,0,255
 
point = rs.AddPoint(a.Origin)

xAxis = rs.AddLine(a.Origin, rs.PointAdd(a.Origin,a.XAxis))
# rs.ObjectColor(xAxis, red)

yAxis = rs.AddLine(a.Origin, rs.PointAdd(a.Origin,a.YAxis))
# rs.ObjectColor(yAxis, green)

zAxis = rs.AddLine(a.Origin, rs.PointAdd(a.Origin,a.ZAxis))
# rs.ObjectColor(zAxis, blue)

