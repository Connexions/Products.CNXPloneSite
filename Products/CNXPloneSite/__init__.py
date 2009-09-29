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


#Monkeypatch Collection.py to include the URL for a CNX specific help files. 
from Products.RhaptosCollection.types import Collection

coldesc = 'Optional: Choose a subtype for this collection. <a href="/help/reference/collection-subtypes">(help)</a>' 
Collection.schema['collectionType'].widget.description=coldesc

subjdesc = 'Select the subject categories that apply to this collection. <a href="/help/reference/subjects">(help)</a>'
Collection.schema['subject'].widget.description=subjdesc 

GoogleAnalyticsTrackingCodeDesc = 'Enter the Google Analytics Tracking Code (e.g. UA-xxxxxxx-x) for this module to track its usage.<br/><em>Note that this code will track only the collection home page, not the modules therein.</em> <a href="/help/reference/GoogleAnalyticsTrackingCode">(help)</a>'
Collection.schema['GoogleAnalyticsTrackingCode'].widget.description=GoogleAnalyticsTrackingCodeDesc

# Make the skins available as DirectoryViews
registerDirectory('skins', globals())

def initialize(context):
    CNXSitePolicy.register(context, product_globals)
