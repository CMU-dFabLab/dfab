"""Top-level package file for the dFab Python library.

Copyright (c) 2014, Garth Zeglin.  All rights reserved. Licensed under the terms
of the BSD 3-clause license as included in LICENSE.
"""

import os

def dfab_package_path():
    """Return the filesystem path to the dFab library install as a string.

    Python will set the dfab.__path__ property to the load path for the dFab
    library.  This allows this function to return a base path for the dFab
    installation, wherever it may happen to be.  This assumes that the full
    subversion tree is intact and installed.
    """
    return os.path.join( __path__[0], "../..")
