## Script (Python) "module_render"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=**kw
##title=displays the CNXML file as part of a module

### cnx_override to set default stylesheet dir ###
kw['stylesheet_path'] = '/cnx-styles/newlook'
### /cnx_override

from Products.RhaptosContent import MODULE_XSL

# Get course options
kw.update(context.getCourseParameters())

if kw.has_key('redirect'):
    if kw['redirect']:
        context.REQUEST.RESPONSE.redirect(context.absolute_url() + '/?collection=%s' % kw['redirect'],301)
        return

source = context.module_export_template(**kw)

# Default XSL stylesheet
if not kw.has_key('stylesheet'):
    kw['stylesheet'] = MODULE_XSL

# Render
body = context.cnxml_transform(source, **kw)

headers = context.REQUEST.RESPONSE.headers
if headers.has_key('last-modified'):
    del headers['last-modified']
context.REQUEST.RESPONSE.setHeader('Cache-Control','no-cache')
return body
