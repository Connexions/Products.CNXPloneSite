from AccessControl import getSecurityManager
from zExceptions import BadRequest

def check(self):
    if not self.meta_type in ("Module Version Folder", "Version Folder"):
        return "Style can only be applied to the pre-version URL of modules and courses."
    if not self.portal_membership.checkPermission('Edit Rhaptos Object', self):
        return "You must be a manager or author/maintainer to set style."
    return None

def specialTIMEA(self):
    retval = check(self)
    if retval is not None:
        return retval

    try:
        self.manage_addProperty('style', '/timea/document.css', 'string')
        self.manage_addProperty('customHeader', 'timea/timeaCustomHeader.htmlf', 'string')
    except BadRequest:
        return "Properties already set on this object."

    return "TIMEA properties have been set. You may return to the content to view changes."

def specialRUP(self):
    retval = check(self)
    if retval is not None:
        return retval

    try:
        self.manage_addProperty('style', '/rup/document.css', 'string')
        self.manage_addProperty('customHeader', 'rup/rupCustomHeader.htmlf', 'string')
    except BadRequest:
        return "Properties already set on this object."

    return "RUP properties have been set. You may return to the content to view changes."
