"""
Connexions site policy definition for customizing Plone at site-creation

Author: Brent Hendricks
(C) 2005 Rice University
All Rights Reserved.
"""

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.Portal import addPolicy
from Products.CMFPlone.interfaces.CustomizationPolicy import ICustomizationPolicy
from Products.RhaptosSite.setup.RhaptosSitePolicy import RhaptosSitePolicy

class CNXSitePolicy(RhaptosSitePolicy):
    """ Customizes the Plone site for Connexions """
    __implements__ = ICustomizationPolicy

    availableAtConstruction=1

    def customize(self, portal):
        # Perform the basic Rhaptos customizations first
        RhaptosSitePolicy.customize(self, portal)
        
        mi_tool = getToolByName(portal, 'portal_migration')
        setup = mi_tool._getWidget('Connexions Setup')
        setup.addItems(setup.available())

def register(context, app_state):
    addPolicy('Connexions Plone site', CNXSitePolicy())

