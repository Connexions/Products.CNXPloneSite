from Products.CMFCore.utils import getToolByName
from Products.Archetypes.Extensions.utils import install_subskin

from Products.CNXPloneSite import product_globals as GLOBALS

from StringIO import StringIO

import zLOG
def log(msg, out=None, severity=zLOG.INFO):
    zLOG.LOG("CNXPloneSite:", severity, msg)
    if out: print >> out, msg

def install(self):
    out = StringIO()
    log("Starting CNXPloneSite install", out)

    log("...installing skins", out)
    install_subskin(self, out, GLOBALS)

    log("...setting caching policies", out)
    cpm = getToolByName(self, 'caching_policy_manager')
    policyids = [x[0] for x in cpm.listPolicies()]
    if "frontpage" not in policyids:
        log("---- adding 'frontpage'", out)
        cpm.addPolicy(policy_id="frontpage",
                      predicate="python:view=='index_html' and object==object.portal_url.getPortalObject()",
                      mtime_func="object/modified",
                      max_age_secs=3601,
                      no_cache=0,
                      no_store=0,
                      must_revalidate=0,
                      vary='',
                      etag_func='',
                      last_modified=0,
                      )
    else:
        log("#### skipping 'frontpage'; already exists", out)

    log("Successfully installed %s." % 'CNXPloneSite', out)
    return out.getvalue()