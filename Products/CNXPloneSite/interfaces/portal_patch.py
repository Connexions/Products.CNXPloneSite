# Copyright (c) 2003 The Connexions Project, All Rights Reserved
# Written by Brent Hendricks, J. Cameron Cooper

""" Patch tool interface"""

from Interface import Attribute
try:
    from Interface import Interface
except ImportError:
    # for Zope versions before 2.6.0
    from Interface import Base as Interface

class portal_patch(Interface):
    """Defines an interface for a tool that provides patch 
    (as in modification based on a diff) capabilities"""

    id = Attribute('id','Must be set to "portal_patch"')

    def createPatch(ob1, ob2, **kw):
        """Create and return a new patch object"""    
    
    def searchPatches(**kw):
        """Find patches with the specified parameters"""

