"""
Connexions-specific setup functions for customizing Plone

Author: Brent Hendricks
(C) 2005 Rice University
All Rights Reserved.

"""

import os
import re
import zLOG
from Acquisition import aq_base

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.Expression import Expression
from Products.CMFCore.DirectoryView import addDirectoryViews

from Products.CNXPloneSite import product_globals
from Products.RhaptosSite.setup.RhaptosSetup import _findObjects

def installProducts(self, portal):
    """Add any necessary portal tools"""
    portal_setup = getToolByName(portal, 'portal_setup')
    import_context = portal_setup.getImportContextID()
    portal_setup.setImportContext(
            'profile-Products.RhaptosBugTrackingTool:default')
    portal_setup.runAllImportSteps()
    portal_setup.setImportContext(
            'profile-Products.FeatureArticle:default')
    portal_setup.runAllImportSteps()
    portal_setup.setImportContext(
            'profile-Products.CNXContent:default')
    portal_setup.runAllImportSteps()
    portal_setup.setImportContext(
            'profile-Products.LensOrganizer:default')
    portal_setup.runAllImportSteps()

    portal_setup.setImportContext(import_context)


def customizeMemberdata(self, portal):
    md = getToolByName(portal, 'portal_memberdata')
    #md._setProperty('comment', '')
    MEMBERDATA_PROPERTIES = (
            ('interests', [], 'lines'),
            ('refer', [], 'lines'),
            ('refertext', '', 'string'),
            ('ok_contact_me', 0, 'boolean'),)

    for prop, default, type in MEMBERDATA_PROPERTIES:
        if not md.hasProperty(prop):
            md._setProperty(prop, default, type)


def customizeActions(self, portal):
    pa_tool=getToolByName(portal,'portal_actions')

    #pa_tool.addAction('qstart', 'Quick Start', 'string:$portal_url/help/', '', 'View', 'site_actions')
    actions = pa_tool._cloneActions()
    for a in actions:
        if a.title == 'MyRhaptos':
            a.title = 'MyCNX'
        if a.title == 'Contact Us':
            a.setActionExpression(
                    Expression('string:$portal_url/aboutus/contact'))
    pa_tool._actions = tuple(actions)

def customizeSkins(self, portal):
    skinstool = getToolByName(portal, 'portal_skins')


    # We need to add Filesystem Directory Views for any directories
    # in our skins/ directory.  These directories should already be
    # configured.
    addDirectoryViews(skinstool, 'skins', product_globals)
    zLOG.LOG("CNXSitePolicy", zLOG.INFO, "Added 'CNXPloneSite' directory view to portal_skins")
    
    # FIXME: we need a better way of constructing this
    pathlist= [p.strip() for p in skinstool.getSkinPath('Rhaptos').split(',')]
    pathlist.insert(1, 'CNXPloneSite')
    pathlist.insert(1, 'cnx_overrides')
    path = ','.join(pathlist)

    # Create a new 'Connexions' skin
    skinstool.addSkinSelection('Connexions', path, make_default=1)
    zLOG.LOG("CNXSitePolicy", zLOG.INFO, "Added 'Connexions' as new default skin")

def customizeTypes(self, portal):
    types_tool=getToolByName(portal,'portal_types')

    # New 'Paper' type based on file
    types_tool.manage_addTypeInformation(id='Paper',
                                         add_meta_type="Factory-based Type Information",
                                         typeinfo_name="CMFDefault: Portal File")
    paper = getattr(types_tool, 'Paper')
    actions=paper._cloneActions()
    for a in actions:
        if a.id == 'edit':
            a.action = Expression('string:${object_url}/paper_edit_form')
    paper._actions=actions

    # New 'Presentation' type based on file
    types_tool.manage_addTypeInformation(id='Presentation',
                                         add_meta_type="Factory-based Type Information",
                                         typeinfo_name="CMFDefault: Portal File")
    pres = getattr(types_tool, 'Presentation')
    pres.manage_changeProperties(content_icon='ppt_icon.png')
    actions=pres._cloneActions()
    for a in actions:
        if a.id == 'edit':
            a.action = Expression('string:${object_url}/presentation_edit_form')
    pres._actions=actions

    # New 'Blog Item' type based on 'News Item'
    types_tool.manage_addTypeInformation(id='Blog Item',
                                         add_meta_type="Factory-based Type Information",
                                         typeinfo_name="CMFDefault: News Item")
    blog = getattr(types_tool, 'Blog Item')
    actions=blog._cloneActions()
    for a in actions:
        if a.id == 'view':
            a.action = Expression('string:${object_url}/blogitem_view')
    blog._actions=actions

    # New 'Blog Folder' type based on 'Folder'
    types_tool.manage_addTypeInformation(id='Blog Folder',
                                         add_meta_type="Factory-based Type Information",
                                         typeinfo_name="CMFPlone: Plone Folder")
    bf = getattr(types_tool, 'Blog Folder')
    actions=bf._cloneActions()
    for a in actions:
        if a.id == 'folderlisting':
            a.visible = 0
        if a.id == 'view':
            a.action = Expression('string:${folder_url}/blogfolder_view')
        a.category = 'object'
    bf._actions=actions


def customizeForms(self, portal):

    # FIXME: This should be redone using CMFFormController
    props_tool=getToolByName(portal,'portal_properties')

    props_tool.form_properties._setProperty('paper_edit_form', 'validate_id,validate_file_edit')
    props_tool.form_properties._setProperty('presentation_edit_form', 'validate_id,validate_file_edit')        
    props_tool.navigation_properties._setProperty('paper.paper_edit_form.success', 'script:file_edit')
    props_tool.navigation_properties._setProperty('paper.paper_edit_form.failure', 'script:paper_edit_form')
    props_tool.navigation_properties._setProperty('presentation.presentation_edit_form.success', 'script:file_edit')
    props_tool.navigation_properties._setProperty('presentation.presentation_edit_form.failure', 'script:presentation_edit_form')


def customizeFrontPage(self, portal):
    if 'index_html' in portal.objectIds():
        portal.manage_delObjects('index_html')
    if 'frontpage' not in portal.objectIds():
        portal.invokeFactory('Document', 'frontpage')
        frontpage = portal.frontpage
        frontpage.title = 'Connexions is:'
        ifile = open(
            os.path.join(os.path.dirname(__file__), 'data', 'frontpage.html'),
            'rb')
        text = ifile.read()
        ifile.close()
        frontpage.edit('html', text)
        portal.setDefaultPage('index_html')

def createAboutusFolder(self, portal):
    if 'aboutus' in portal.objectIds() and 'placeholder' in portal.aboutus.objectIds():
        portal.manage_delObjects('aboutus')

    if 'aboutus' not in portal.objectIds():
        portal.invokeFactory('Folder', 'aboutus')
        folder = portal.aboutus
        folder.setTitle('About')
        folder.invokeFactory('Document', 'contact')
        contact = folder.contact
        contact.setTitle('Contact Us')
        ifile = open(
            os.path.join(os.path.dirname(__file__), 'data', 'contact.html'),
            'rb')
        text = ifile.read()
        ifile.close()
        contact.edit('html', text)
        
        folder.invokeFactory('Document', 'index_html')
        index = folder.index_html
        index.setTitle('Philosophy')
        index.setDescription('The Connexions approach')
        ifile = open(
            os.path.join(os.path.dirname(__file__), 'data', 'philosophy.stx'),
            'rb')
        text = ifile.read()
        ifile.close()
        index.edit('text/structured', text)

def createContent(self, portal):
    if 'sitelicense' not in portal.objectIds():
        portal.invokeFactory('Document', 'sitelicense')
        license = portal.sitelicense
        license.setTitle('Connexions Service and Repository User Agreement')
        ifile = open(
            os.path.join(os.path.dirname(__file__), 'data', 'sitelicense.stx'),
            'rb')
        text = ifile.read()
        ifile.close()
        license.edit('text/structured', text)

def customizePortlets(self, portal):
    left_slots = [
            'here/portlet_navigation/macros/portlet',
            ]

    portal.manage_changeProperties(left_slots=left_slots)

functions = {
    'Install Products': installProducts,
    'Customize Member Data': customizeMemberdata,
    'Customize Actions': customizeActions,
    'Customize Skins': customizeSkins,
    'Customize Types': customizeTypes,
# XXX commented this out because it is broken and doesn't appear to be used
#    'Customize Forms': customizeForms,
    'Create About Us folder': createAboutusFolder,
    'Customize Front Page': customizeFrontPage,
    'Create Content': createContent,
    'Customize Portlets': customizePortlets,
    }

class CNXSetup:
    type = 'Connexions Setup'

    description = "Site customizations for Connexions"

    functions = functions

    ## This line and below may not be necessary at some point
    ## in the future. A future version of Plone may provide a
    ## superclass for a basic SetupWidget that will safely
    ## obviate the need for these methods.
     
    single = 0
  
    def __init__(self, portal):
        self.portal = portal
  
    def setup(self):
        pass
 
    def delItems(self, fns):
        out = []
        out.append(('Currently there is no way to remove a function', zLOG.INFO))
        return out
 
    def addItems(self, fns):
        out = []
        for fn in fns:
            self.functions[fn](self, self.portal)
            out.append(('Function %s has been applied' % fn, zLOG.INFO))
        return out
 
    def active(self):
        return 1
                                                                                 
    def installed(self):
        return []
 
    def available(self):
        """ Go get the functions """
        # We return an explicit list here instead of just functions.keys() since order matters
        return [
            'Install Products',
            'Customize Member Data',
            'Customize Actions',
            'Customize Skins',
            'Customize Types',
#            'Customize Forms',
            'Create About Us folder',
            'Customize Front Page',
            'Create Content',
            'Customize Portlets',
            ]
