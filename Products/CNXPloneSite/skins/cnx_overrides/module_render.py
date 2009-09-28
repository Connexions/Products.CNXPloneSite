## Script (Python) "module_render"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=**kw
##title=displays the CNXML file as part of a module
from Products.RhaptosContent import MODULE_XSL
from Products.RhaptosContent import MODULE_XSL_OLD

### cnx_override to set default stylesheet dir ###
kw['stylesheet_path'] = '/cnx-styles/newlook'
### /cnx_override

# Get course options
kw.update(context.getCourseParameters())

source = context.module_export_template(**kw)

# Default XSL stylesheet
if not kw.has_key('stylesheet'):
    kw['stylesheet'] = MODULE_XSL

# use the old XSLT until such time as the CSS can handle the new structure
styleList = ('/rup/document.css','/timea/document.css', '/rup/document.sale.css',
             'http://cnx.org/ncpea/document.css', 'http://cnx.org/twb/document.css',
             '/ncpea/document.css', '/twb/document.css')
simpleProperty = getattr(context, 'style', None) in styleList
paramProperty = getattr(context, 'getParameters', lambda:{})().get('style', None) in styleList
courseProperty = getattr(context, 'getCourseParameters', lambda:{})().get('style', None) in styleList

if simpleProperty or paramProperty or courseProperty:
   #kw['stylesheet_path'] = '/cnx-styles/sky'
   kw['stylesheet'] = MODULE_XSL_OLD

# Render
body = context.cnxml_transform(source, **kw)

headers = context.REQUEST.RESPONSE.headers
if headers.has_key('last-modified'):
    del headers['last-modified']
context.REQUEST.RESPONSE.setHeader('Cache-Control','no-cache')
return body

