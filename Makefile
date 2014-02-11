# @file Makefile
#
# @brief Top-level dFab build control file.
#
# @remarks This isn't a proper dependency-driven makefile.

default: doc

# Build the auto-generated html source code documentation.
doc: html-docs
	doxygen documentation/Doxyfile

html-docs: ; mkdir $@

# Open the generated documentation locally.
read:
	firefox html-docs/index.html &

# Start up a documentation web server.  Note that this isn't very robust or
# secure, but is fine for browsing the documents from another machine.  Just
# don't leave it running.
doc-server:
	cd html-docs/html ; python -m SimpleHTTPServer 8000 &

