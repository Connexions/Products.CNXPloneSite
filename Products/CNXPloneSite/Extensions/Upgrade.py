from Products.CMFCore.utils import getToolByName
from Products.CMFCore.Expression import Expression
from Products.CMFCore.permissions import SetOwnProperties
from Acquisition import aq_base
import transaction
from StringIO import StringIO

SKIN_PATHS = [
'custom',
'CNXPloneSite',
'cnx_overrides',
'CNXMLFile',
'RisaModuleEditor',
'RisaWorkgroup',
'FeatureArticle',
'risacollection',
'CNXContent',
'ChangeSet',
'RisaRepository',
'RisaHitCountTool',
'PasswordReset',
'archetypes',
'gruf',
'mimetypes_icons',
'plone_ecmascript',
'plone_wysiwyg',
'plone_3rdParty/CMFTopic',
'plone_templates',
'plone_styles',
'plone_scripts',
'plone_portlets',
'plone_form_scripts',
'plone_prefs',
'plone_forms',
'plone_images',
'plone_content',
'ordered_plone_folder',
'cmf_legacy',
]


portal = None

def migrateContentPointerUID(obj, path):
    global portal
    #global count
    objUID = getattr(aq_base(obj), '_uid', None)        
    if objUID is not None: #continue    # not an old style AT?
        setattr(obj, 'old_tmp_at_uid', objUID) # this one can be part of the catalog
        delattr(obj, '_uid')
        setattr(obj, '_at_uid', None)
    obj._register()            # creates a new UID
    obj._updateCatalog(portal) # to be sure
    #count+=1
    # avoid eating up all RAM
    #if not count % 250:
    #    transaction.commit(1)

def folderConvert(folder, portal_type='Folder'):
    id = folder.getId()
    parent = folder.aq_parent
    parent.manage_renameObject(id, 'temp')
    parent.invokeFactory(id=id, type_name=portal_type)
    target = getattr(parent, id)
    folder = getattr(parent, 'temp')
    order = folder.objectIds()
    target.manage_pasteObjects(folder.manage_cutObjects(order))
    if 'index_html' in order and 'copy_of_index_html' in target.objectIds():
        target.manage_renameObject('copy_of_index_html', 'index_html')
    target.workflow_history['folder_workflow']=folder.workflow_history['plone_workflow']
    target._updateProperty('title', folder.title)
    target.setDescription(folder.description)
    parent.manage_delObjects(['temp'])

def upgrade_skins(self):
    """Upgrade the skins tool"""
    skins_tool = getToolByName(self, 'portal_skins')
    skins_tool.manage_addProduct['CMFCore'].manage_addDirectoryView('CNXPloneSite/skins/cnx_overrides')
    skins_tool.manage_delObjects(['Images', 'actionicons', 'calendar', 'control', 'generic', 'no_css', 'nouvelle', 'topic', 'zpt_calendar', 'zpt_content', 'zpt_control', 'zpt_generic', 'zpt_topic'])
    skins_tool.selections['Connexions'] = ','.join(SKIN_PATHS)
    skins_tool.default_skin = 'Connexions'
    skins_tool._p_changed = 1

def register_hit_counts(self):
    """Register current objects with the hitcount tool"""
    h_tool = getToolByName(self, 'portal_hitcount')
    
    for objectId, date in self.devrep().query("SELECT moduleid, min(revised) from modules group by moduleid")[1]:
        h_tool.registerObject(objectId, date)

    for objectId, f in self.content.objectItems():
        h_tool.registerObject(objectId, f.getHistory()[-1].revised)


def migrateInterestsToLines(self):

    mdtool = getToolByName(self,'portal_memberdata')
    if mdtool.hasProperty('interests'):
        mdtool._delProperty('interests')
    mdtool._setProperty('interests', (), 'lines')
            
    mems = mdtool.objectValues()
    for mem in mems:
        if type(mem.interests) == type(''):
            mem.interests = tuple(mem.interests.split(','))

def fixHomepageURLs(self):
    """Add an http: to the beginning of homepage values that currently do not have it"""
    mdtool = getToolByName(self,'portal_memberdata')
    mems = mdtool.objectValues()
    for mem in mems:
        homepage = mem.homepage
        if homepage:
            homepage = homepage.strip()
            if not homepage.lower().startswith('http://'):
                if homepage.find('://') == -1:
                    homepage = 'http://' + homepage
            mem.homepage = homepage
                    
    
def upgrade(self):
    """Upgrade Risa Plone Site"""
    out = StringIO()
    out.write("Upgrading Risa Repository\n")

    global portal
    portal = self

    # Pre-migration work so it will succeed
    out.write("Pre-migration\n")
    skins_tool = getToolByName(self, 'portal_skins')
    skins_tool.manage_delObjects(['content'])
    skins_tool.custom.manage_delObjects(skins_tool.custom.objectIds())

    # Do plone migration
    out.write("Plone migration\n")
    mig_tool = getToolByName(self, 'portal_migration')
    mig_tool.upgrade()

    # Post-plone migration, change memberdata tool back to ours
    out.write("Fixing memberdata tool\n")
    orig_md = getToolByName(self, 'portal_memberdata')
    self.manage_delObjects('portal_memberdata')
    self.manage_addProduct['CNXPloneSite'].manage_addTool('SQL Member Data Tool')
    md = getToolByName(self, 'portal_memberdata')
    _actions = getattr(orig_md, '_actions')
    md._actions = aq_base(_actions)
    _members = getattr(orig_md, '_members')
    md._members = aq_base(_members)
    _properties = getattr(orig_md, '_properties')
    md._properties = aq_base(_properties)
    for attr in orig_md.propertyIds():
        setattr(md, attr, aq_base(getattr(aq_base(orig_md), attr)))

    # Reinstall Products
    out.write("Product migration\n")
    qi = getToolByName(self, 'portal_quickinstaller')
    qi.reinstallProducts(['Archetypes', 'RisaModuleEditor', 'RisaCollection'])

    # Archetypes migration
    out.write("AT migration\n")
    at_tool = getToolByName(self, 'archetype_tool')
    at_tool.manage_migrate()
    self.REQUEST.form['FeatureArticle.FeatureArticle'] = True
    self.REQUEST.form['FeatureArticle.UserFeedback'] = True
    at_tool.manage_updateSchema(self.REQUEST)

    catalog = getToolByName(self, 'portal_catalog')
    catalog.ZopeFindAndApply(self, obj_metatypes=['PublishedContentPointer'], search_sub=True, apply_func=migrateContentPointerUID)


    # Migrate portlets
    out.write("Portlet migration\n")
    left_slots=['here/portlet_navigation/macros/portlet',
                'here/workspaces_slot/macros/portlet',
                'here/portlet_login/macros/portlet'
                ]

    right_slots=['here/portlet_pending/macros/portlet',
                 'here/portlet_news/macros/portlet',
                 'here/portlet_review/macros/portlet'
                 ]

    self._updateProperty('right_slots', right_slots)
    self._updateProperty('left_slots', left_slots)
    right_slots = ['here/portlet_pending/macros/portlet',
                   'here/log_action_slot/macros/portlet']

    self.Members._updateProperty('right_slots', right_slots)
    self.GroupWorkspaces._updateProperty('right_slots', right_slots)


    # Migrate portal
    out.write("Portal migration\n")
    # Work around bug in PloneTool.browserDefault() where skins
    # don't get searched for default pages unless they're
    # explictly set as a property
    self._setProperty('default_page', 'index_html')

    self.content._updateProperty('title', 'Content')

    prop_tool=getToolByName(self, 'portal_properties')
    prop_tool.navtree_properties._updateProperty('croppingLength', 18)

    # Migrate syndication
    syn_tool=getToolByName(self, 'portal_syndication')
    syn_tool.isAllowed = 1

    # Migrate actions
    out.write("Action migration\n")
    pa_tool=getToolByName(self, 'portal_actions')
    for a in pa_tool._actions:
        if a.id in ('Members', 'news', 'search_form', 'change_status', 'small_text', 'normal_text', 'large_text', 'sendto', 'print', 'addtofavorites'):
            a.visible = 0
        elif a.id == 'qstart':
            a.category = 'site_actions'
        elif a.id == 'courses':
            a.action = Expression('string:$portal_url/content/browse_course_titles')
            a.category = 'site_actions'
        elif a.id == 'index_html':
            a.action = Expression('string:${portal_url}/')
        elif a.id == 'bugreport':
            a.category = 'user'
        elif a.id == 'extedit':
            a.condition = Expression("python: hasattr(portal.portal_properties.site_properties, 'ext_editor') and portal.portal_properties.site_properties.ext_editor and object.absolute_url() != portal_url and not getattr(object,'isPrincipiaFolderish',None)")

    pa_tool._p_changed = 1

    m_tool = getToolByName(self, 'portal_membership')
    for a in m_tool._actions:
        if a.id == 'preferences':
            a.title = 'My Account'

    m_tool._p_changed = 1

    undo_tool=getToolByName(self,'portal_undo')
    for a in undo_tool._actions:
        a.visible = 0

    undo_tool._p_changed = 1

    # Migrate types
    out.write("Types migration\n")

    # New 'FeedbackFolder' now based on 'PloneFolder'
    types_tool = getToolByName(self, 'portal_types')
    types_tool.manage_delObjects('FeedbackFolder')
    types_tool.manage_addTypeInformation(id='FeedbackFolder',
                                         add_meta_type="Factory-based Type Information",
                                         typeinfo_name="CMFPlone: Plone Folder")
    ff = getattr(types_tool, 'FeedbackFolder')
    for a in ff._actions:
        if a.id == 'view':
            a.action = Expression('feedbackfolder_view')

    ff._p_changed = 1
    ff.filter_content_types = 1
    ff.allowed_content_types = ('UserFeedback')

    for portal_type in ['Connexions Workgroup', 'Collection', 'Module', 'CNXML Document', 'Image', 'File', 'SubCollection', 'PublishedContentPointer','Repository']:
        t = getattr(types_tool, portal_type)
        for a in t._actions:
            if a.id == 'local_roles':
                a.visible = 0
        t._p_changed = 1

    # Use factory tool now
    fac_tool = getToolByName(self, 'portal_factory')
    fac_tool.manage_setPortalFactoryTypes(listOfTypeIds=['Collection', 'Module', 'Image', 'File'])


    # Migrate folders
    out.write("Folder migration\n")
    folderConvert(self.aboutus.inthenews)
    folderConvert(self.aboutus.publications)
    folderConvert(self.feedback, 'FeedbackFolder')


    # Migrate control panel
    out.write("Control panel migration\n")
    groups = ['site|Plone|Plone Configuration',
              'site|Products|Add-on Product Configuration',
              'member|Member|Account Maintenance',
              'member|Collaboration|Collaboration Requests',
              'member|Content|Content'
              ]

    configlets = (
        {'id':'Collaborations',
         'appId':'Collaborations',
         'name':'Role Requests',
         'action':'string:${portal_url}/collaborations',
         'permission': SetOwnProperties,
         'category':'Collaboration',
         },
        {'id':'Patches',
         'appId':'Patches',
         'name':'Suggested Edits',
         'action':'string:${portal_url}/patches',
         'permission': SetOwnProperties,
         'category':'Collaboration',
         },
        {'id':'content',
         'appId':'Content',
         'name':'My Content',
         'action':'string:${portal_url}/content/by_author/${member}',
         'permission': SetOwnProperties,
         'category':'Content',
         },

        )
    cp_tool = getToolByName(self, 'portal_controlpanel')
    cp_tool._updateProperty('groups', groups)
    cp_tool.registerConfiglets(configlets)

    # Migrate permissions
    out.write("Permission migration\n")
    self.Members.manage_permission('Add Annotation Servers', ('Manager', 'Owner',), acquire=1)
    self.Members.manage_permission('View', ('Manager', 'Owner',), acquire=0)
    self.Members.manage_permission('List folder contents', ('Manager', 'Owner',), acquire=0)

    self.GroupWorkspaces.manage_permission('Add Annotation Servers', ('Manager', 'Owner',), acquire=1)
    self.GroupWorkspaces.manage_permission('View', ('Manager', 'Owner',), acquire=0)
    self.GroupWorkspaces.manage_permission('List folder contents', ('Manager', 'Owner',), acquire=0)

    # Install and populate hit-count tool
    out.write("Installed HitCount tool\n")
    qi.installProducts(['RisaHitCountTool'])
    register_hit_counts(self)

    # Migrate skins
    out.write("Skin migration\n")
    upgrade_skins(self)
    
    return out.getvalue()

def fixUserStatus(self):
    """Some old users do not have a status field and thus cannot display their member profile"""
    mdtool = getToolByName(self,'portal_memberdata')
    mems = mdtool.objectValues()
    for mem in mems:
        if mem.status == '':
            mem.status='Approved'

def removeCountsFromFrontpage(self):
    """Remove the last paragraph of the homepage so that it can be split into a dynamic pagetemplate"""
    fp=self.frontpage
    ind = fp.text.find('\t<h2>Connexions is growing')
    if ind != -1:
        fp.manage_editDocument(text=fp.text[:ind],text_format='html')
