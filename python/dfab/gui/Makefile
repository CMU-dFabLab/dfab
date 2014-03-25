## @file Makefile
## @brief Generate the PyQt4 GUI Python object sources from the Qt Designer .ui files.
## This must be manually invoked with 'make' whenever the Qt Designer files are updated.
##
## @copyright Copyright (c) 2014, Garth Zeglin. All rights reserved. Licensed
##            under the terms of the BSD 3-clause license as included in
##            LICENSE.

default: MocapProcessDialog.py RobotConsoleWindow.py

# This is currently using the MacPorts version of pyuic4, hence the -2.7 suffix.

%.py: %.ui
	pyuic4-2.7 $^ >$@
