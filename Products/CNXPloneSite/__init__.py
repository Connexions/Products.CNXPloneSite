"""
Connexions Site Customization

Author: Brent Hendricks
(C) 2005 Rice University
All Rights Reserved.
"""

# We define this first so that CNXSetup can import it w/o recursion
product_globals = globals()

import sys
from Products.CMFCore.DirectoryView import registerDirectory

import MembershipTool

from setup import CNXSitePolicy

this_module = sys.modules[ __name__ ]


# Make the skins available as DirectoryViews
registerDirectory('skins', globals())

def initialize(context):
    CNXSitePolicy.register(context, product_globals)
