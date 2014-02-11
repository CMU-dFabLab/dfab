"""Optitrack Motion Capture CSV File Parser.

@authors  luke.s.metz@gmail.com
          Aaron Hoover <amhoov@gmail.com>
          Franklin W. Olin College of Engineering

--- change log -------------------------------------------------------

Jan 2014: Updated by Garth Zeglin for Optitrack CSV file format 1.1.

It appears there was a change in terminology: the current 1.1 format appears to
use 'rigidbody' where the previous format used 'trackable'.  The code still uses
the 'trackable' terminology.

The original version was downloaded from github using the following:
  git clone https://github.com/OlinRoboticsAndBioinspiration/mocap.git

--- original copyright notice ---------------------------------------

* Copyright (c) 2014, Franklin W. Olin College of Engineering

* All rights reserved.

* Redistribution and use in source and binary forms, with or without
* modification, are permitted provided that the following conditions are met:

* - Redistributions of source code must retain the above copyright notice,
* this list of conditions and the following disclaimer.

* - Redistributions in binary form must reproduce the above copyright notice,
* this list of conditions and the following disclaimer in the documentation
* and/or other materials provided with the distribution.

* - Neither the name of Franklin W. Olin College of Engineering nor the names
* of its contributors may be used to endorse or promote products derived
* from this software without specific prior written permission.

* THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
* AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
* IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
* ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
* LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
* CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
* SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
* INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
* CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
* ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
* POSSIBILITY OF SUCH DAMAGE.

"""

import os
import csv
import numpy as np

TSL = 11        # trackable state vector length
MSL = 5         # marker state vector

bad = '#'

################################################################
class Run():
    """Represents a motion capture run as a collection of frame objects holding the complete state at each time sample.

    Object attributes:
    trackables         list of Trackable objects with rigid body definitions
    frames             list of Frame objects with motion capture body and marker positions
    trackable_frames   list of TrackableFrame objects with extended data on frame
    coord_type         coordinate system convention, either 'left' or 'right'
    framecount         the number of frames present in file
    trackablecount     the number of rigid bodies represented in file
    """

    def __init__(self):
        self.trackables = []
        self.frames = []
        self.trackable_frames = []
        self.coord_type = 'right'
        self.framecount = 0
        self.trackablecount = 0

        self.dir = None
        self.fi  = None


    def trk(self,id=None,name=None):
      """
      t,d = trk()

      Return marker data for trackable, specifying either id or name

      t - 1 x N - timestamp for N frames
      d - N x M x 3 - x,y,z data for M markers in N frames
      """
      ids = [t.id for t in self.trackables]
      names = [t.name for t in self.trackables]
      try:
        int(id)
      except:
        name = id
        id = None
      if name in names:
        id = ids[names.index(name)]
      #TODO ensure it only works with some set of markers. Re add functionality of `assert not(id is None)`
      if id == None:
        trackable = Trackable()
        trackable.name = name
        trackable.id = len(self.trackables)+1
        id = trackable.id
        ids.append (id)
        self.trackables.append(trackable)

      tr = self.trackables[ids.index(id)]
      N = len(self.frames)

      #TODO make this not depend on the first frame
      M = len(self.trackable_frames[0].ptcld_markers) #get the length from the first frame

      t = np.nan*np.zeros(N)
      d = np.nan*np.zeros((N,M,3))

      for f in self.trackable_frames:
        if f.id == id:
          j = f.index
          t[j] = f.timestamp

          data = np.asarray([m.pos.toArray() for m in f.ptcld_markers]);
          #for now ignore all non perfect data
          if data.shape[0] == M:
            d[j,:,:] = np.asarray([m.pos.toArray() for m in f.ptcld_markers])

      return t,d

    #---------------------------------------------------------------
    def data(self):
      """
      t,d,D,S = data()

      Return data

      t - 1 x N - timestamp for N frames
      d - N x M x 3 - x,y,z data for M markers in N frames
      D - N x M_l x 3 - x,y,z data for M_l markers in N frames from trackable l
      S - N x L x 6 - yaw,pitch,roll,x,y,z data for L trackables in N frames
      """
      if not self.frames:
        return None,None,None,None
      #t,d = zip(*[(f.timestamp,[m.pos.toArray() for m in f.markers]) 
      #                                         for f in self.frames])
      #t = [f.timestamp for f in self.frames]
      #d = [[m.pos.toArray() for m in f.markers] for f in self.frames]
      t = []; d = []; D = [];
      S = np.nan*np.zeros((len(self.frames),self.trackablecount,6))
      for j,f in enumerate(self.frames):
          t.append(f.timestamp)
          d.append([m.pos.toArray() for m in f.markers])
          for s in f.trackable_states:
              S[j,s.id-1,:] = np.hstack((s.erot.toArray(),s.pos.toArray()))


      m = [len(dd) for dd in d]
      M = max(m)
      p = [np.nan*np.ones(3) for m in range(M)]

      d = [dd + p[len(dd):] for dd in d]

      return np.array(t),np.array(d),D,np.array(S)

    #---------------------------------------------------------------
    def trajectory(self, name, warnings=5 ):
        """Return the trajectory of a rigid body.
      
        Returns t vector and x,q,ypr matrices
        t - 1 x N - timestamp for N frames
        x - N x 3 - x,y,z centroid path for N frames
        q - N x 4 - qx, qy, qz, qw quaternion orientation for N frames.
        ypr - N x 3 - yaw, pitch, roll, Euler angle sets for N frames.
        """
      
        # determine the index of the body within the list of rigid bodies
        names = [t.name for t in self.trackables]
        body_idx = names.index(name)
        
        # determine the body ID number reported with each frame
        body_id  = self.trackables[body_idx].id

        t = []
        x = []
        q = []
        ypr = []

        warning_count = 0

        for i,f in enumerate(self.frames):
            # check whether the body appears in this frame
            try:
                idx = [state.id for state in f.trackable_states].index(body_id)
                t.append(f.timestamp)
                state = f.trackable_states[idx]
                x.append( state.pos.toArray() )
                q.append( state.qrot.toArray( ) )
                ypr.append( state.erot.toArray() )

            except ValueError:
                warning_count += 1
                if warnings and warning_count <= warnings:
                    print "Body '%s' does not appear in frame %d." % (name, i)                    
                    if warning_count == warnings: print "(Additional warnings for '%s' will be suppressed.)" % name

                pass

        return np.array(t), np.array(x), np.array(q), np.array(ypr)

    #---------------------------------------------------------------
    def ReadFile(self, data_dir, filename, N=np.inf, verbose=False):
        """Load a CSV motion capture data file.

        Args:
            data_dir: string directory name
            filename: string name of the file to load

        Keyword arguments:
        N -- maximum number of frames to process (default unlimited).
        verbose -- flag to enable debugging console output (default False). 
        """

        self.dir = data_dir
        self.fi  = filename
        filename = os.path.join(data_dir, filename)
        fp = csv.reader(open(filename, "rU"))
        try:
          while True:
              if len( self.frames ) >= N:
                  break
              fields = fp.next()
              if verbose: print "CSV input: ", fields

              # the first field of every CSV line indentifies the row type
              row_type = fields[0].lower()

              if row_type == "comment":
                  pass

              elif row_type == "righthanded":
                  self.coord_type = 'right'

              elif row_type == "lefthanded":
                  self.coord_type = 'left'

              elif row_type == "info":
                  if fields[1].lower() == "framecount":
                      self.framecount = int(fields[2])

                  elif verbose and fields[1].lower() == "version":
                      print "File format version", fields[2]

                      # For now, just fail if the Optitrack file format version
                      # is different.  If the Optitrack software is updated,
                      # this might need to change.  Note that the format is
                      # already different than the original Olin code, but it
                      # isn't clear what Optitrack file version was used to
                      # create that code.
                      assert fields[2] == '1.1', "Optitrack file format %s not tested." % fields[2]


                  # N.B. the 'rigidbody' token can identify one of two possible
                  # record types, either a body definition immediately following
                  # the info section, or an extended information record
                  # following a frame.  The following block processes the set of
                  # body definitions; it makes the assumption that
                  # rigidbodycount is always the last info field.
                  elif fields[1].lower() == "rigidbodycount":
                      self.trackablecount = int(fields[2])
                      if self.trackablecount > 0:
                          for i in range(self.trackablecount):
                              self.trackables.append(Trackable(fp.next()))

              elif row_type == "frame":
                  self.frames.append(Frame(fields))

              # FIXME: the following would process the extended frame information, but it is currently broken
              # elif row_type == "rigidbody":
              #   self.trackable_frames.append(TrackableFrame(fields))

        except StopIteration:
            pass

    def __repr__( self ):
      return "run = {'dir':%s,'fi':%s}" % (self.dir,self.fi)

################################################################
class Frame():
    """Represents one frame of motion capture data"""
    def __init__(self, fields):
        """Constructor for a frame object"""
        if fields[0].lower() != "frame":
            raise Exception("You attempted to make a frame from something " +\
                            "that is not frame data.")

        self.trackable_states = []
        self.markers = []

        self.index = int(fields[1])             # frame index (integer count)
        self.timestamp = float(fields[2])       # time stamp (in seconds)
        self.trackable_count = int(fields[3])   # number of rigid bodies tracked in current frame

        # starting in field 4 is a set of fields per rigid body:
        #    Rigid Body ID, Position, Quaternion Orientation, and Euler Angle Orientation (ID, x,y,z, qx, qy, qz, qw, yaw, pitch, roll)
        
        idx = 4
        if self.trackable_count > 0:
            for i in range(self.trackable_count):
                if not( bad in ''.join(fields[idx:idx+TSL]) ):
                    self.trackable_states.append(TrackableState(fields[idx:idx+TSL]))
                idx += TSL


        # following the rigid body fields is the marker count:
        self.marker_count = int(fields[idx])
        idx += 1

        # following the marker count is a set of fields per marker:
        #   x,y,z,id,name
        for i in range(self.marker_count):
            if not( bad in ''.join(fields[idx:idx+MSL]) ):
                self.markers.append(Marker( id=fields[idx+3], pos=fields[idx:idx+3], name=fields[idx+4]))
            idx += MSL

    def __repr__( self ):
      return "frame = {'index':%s,'t':%f,'m':%d,'l':%d}" % (self.index,self.timestamp,len(self.markers),self.trackable_count)

class TrackableFrame():
    """Represents extended frame information for frames containing
    rigid bodies."""

    def __init__(self, fields):
        """Constructor for a frame of extended trackable information"""
        self.markers = []
        self.ptcld_markers = []
        self.index = int(fields[1])
        self.timestamp = float(fields[2])
        self.name = fields[3]
        self.id = int(fields[4])
        self.last_tracked = int(fields[5])
        self.marker_count = int(fields[6])
        idx = 7
        #Store the trackable markers
        for i in range(self.marker_count):
            tracked = fields[idx + (self.marker_count-i)*MSL + self.marker_count*MSL +
                             i]
            quality = fields[idx + (self.marker_count-i)*MSL +
                             self.marker_count*MSL + self.marker_count + i]
            if not( bad in ''.join(fields[idx:idx+MSL]) ):
              self.markers.append(TrackableMarker(None, fields[idx:idx+MSL], tracked, quality))
            idx += MSL
        #Store the point cloud markers
        for i in range(self.marker_count):
            if not( bad in ''.join(fields[idx:idx+MSL]) ):
                self.ptcld_markers.append(Marker(None, fields[idx:idx+MSL]))
            idx += MSL

        self.mean_error = np.nan
        if not( bad in ''.join(fields[idx + 2*self.marker_count]) ):
            float(fields[idx + 2*self.marker_count])

    def __repr__( self ):
      return "trk_frame = {'index':%s,'id':%s,'t':%f,'name':%s,'m':%d}" % (self.index,self.id,self.timestamp,self.name,len(self.ptcld_markers))

################################################################
class Marker():
    """Represent a motion capture marker as an indexed, named point in 3D space."""

    def __init__(self, id, pos, name=None):
        """Constructor for a marker object."""
        self.id = int(id)
        self.name = name
        self.pos = Position(pos)

    def __repr__( self ):
      return "marker = { 'name': '%s', 'id':%d,'pos':%s}" % ( self.name, self.id, self.pos )

################################################################
class TrackableMarker(Marker):
    """An extended marker with some data related to tracking"""

    def __init__(self, id, pos, tracked, quality):
        """Constructor for a trackable marker"""
        Marker.__init__(self, id, pos)
        self.tracked = tracked
        self.quality = quality

    def __repr__( self ):
      return "trk_" + Marker.__repr__(self)

class TrackableState():
    """Represents the dynamic state of a trackable object"""

    def __init__(self, fields):
        """Constructor for a trackable state object"""
        self.id = int(fields[0])
        self.pos = Position(fields[1:4])
        self.qrot = QRot(fields[4:8])
        self.erot = ERot(fields[8:11])

    def __repr__( self ):
      return "trk_state = {'id':%d,'pos':%s,'erot':%s}" % (self.id,self.pos,self.erot)

################################################################
class Trackable():
    """Represents a rigid body.

    Attributes:
    name        -- string
    id          -- numeric index
    num_markers -- number of markers in body
    markers     -- list of Position vectors defining each marker position in body
    """

    def __init__(self, fields=None):
        """Constructor for a trackable object"""
        self.name = None
        self.id = None
        self.num_markers = 0
        self.markers = []
        
        if fields == None:
			return;
        
        if fields[0].lower() != "rigidbody":
            raise Exception("You attempted to make a trackable object from " +\
                            "data that does not represent a rigidbody.")

        self.name = fields[1]
        self.id = int(fields[2])
        self.num_markers = int(fields[3])
        self.markers = []
        idx = 4

        # Each marker definition follows as a (x,y,z) vector within the rigid body frame.
        for i in range(self.num_markers):
            self.markers.append(Position(fields[idx:idx+3]))
            idx += 3

    def __repr__( self ):
      return "trk = {'id':%d,'name':%s,'m':%d}" % (self.id,self.name,self.num_markers)

################################################################
class Position():
    """A class representing the x,y,z position of a point in space"""

    def __init__(self, fields):
        """Constructor of for a position object"""

        self.x = float(fields[0])
        self.y = float(fields[1])
        self.z = float(fields[2])

    def toArray(self):
        return np.array([self.x, self.y, self.z])

    def __repr__( self ):
      return "[%f,%f,%f]" % (self.x,self.y,self.z)

class QRot():
    """A class representing a rotation using Quaternions"""

    def __init__(self, fields):
        """Constructor for a quaternion-based rotation"""
        self.qx = float(fields[0])
        self.qy = float(fields[1])
        self.qz = float(fields[2])
        self.qw = float(fields[3])

    def toArray(self):
        return np.array([self.qx, self.qy, self.qz, self.qw])

class ERot():
    """A class representing a rotation using Euler angles"""

    def __init__(self, fields):
        """Constructor for an Euler angle-based rotation using the 3-2-1 or
        yaw, pitch, roll sequence"""
        self.yaw = float(fields[0])
        self.pitch = float(fields[1])
        self.roll = float(fields[2])

    def toArray(self):
        return np.array([self.yaw, self.pitch, self.roll])

    def __repr__( self ):
      return "[%f,%f,%f]" % (self.yaw,self.pitch,self.roll)
