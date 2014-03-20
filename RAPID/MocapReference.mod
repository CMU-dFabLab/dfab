! Drive the ABB to the standard location for Optitrack Motion Capture calibration.
! The 4-marker 300-400-500 mm reference should be mounted.
MODULE MocapReference
   PERS tooldata testtool := [TRUE,[[0,0,-61.5138],[1,0,0,0]],[1,[0,-0.0001,0],[1,0,0,0],0,0,0]];
   VAR speeddata myspeed := [200,100,200,1000];
   CONST robtarget Target0:=[[100.00,1500.00,1400.00],[0.707106781186548,0,0,0.707106781186547],[1,0,1,0],[2000.00,9E9,9E9,9E9,9E9,9E9]];
   PROC testproc()
      ConfJ \Off;
      ConfL \Off;
      MoveL Target0,myspeed,z1,testtool \Wobj:=WObj0;
   ENDPROC
ENDMODULE
