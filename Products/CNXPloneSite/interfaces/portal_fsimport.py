# Copyright (c) 2003 The Connexions Project, All Rights Reserved
# Written by Brent Hendricks

""" File system import interface"""

from Interface import Attribute
try:
    from Interface import Interface
except ImportError:
    # for Zope versions before 2.6.0
    from Interface import Base as Interface

class portal_fsimport(Interface):
    """Defines an interface for a tool that provides import/export
    facilities between the ZODB and the filesystem"""

    id = Attribute('id','Must be set to "portal_fsimport"')

    def exportFolder(obj, path='', includeSelf=1):
        """Export a ZODB folder to the file system""" 
        
    def exportFile(obj, path=None):
        """Export a ZODB file to the file system"""

    def importFolder(path, container):
        """Recursively import the contents of a filesystem directory into the specified ZODB container"""
    
    def importFile(filename, container):
        """Import a file into the specified ZODB container"""
    

