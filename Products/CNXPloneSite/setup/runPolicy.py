
from Products.CMFCore.utils import getToolByName

def runPolicy(context):
    logger = context.getLogger('cnxplonesite')
    if context.readDataFile('cnxplonesite.txt') is None:
        logger.info('Nothing to import.')
        return
    portal = context.getSite()
    # XXX run the rhaptos profile from here. Should be a dependency in 
    # metadata.xml but the GenericSetup version that is used does not support
    # metadata.xml
    portal_setup = getToolByName(portal, 'portal_setup')
    import_context = portal_setup.getImportContextID()
    portal_setup.setImportContext(
            'profile-RhaptosSite:rhaptos-default')
    portal_setup.runAllImportSteps()
    portal_setup.setImportContext(import_context)

    portal_migration = getToolByName(portal, 'portal_migration')
    setup = portal_migration._getWidget('Connexions Setup')
    setup.addItems(setup.available())
