## Script (Python) "fileSizeUnits"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=filesize
##title=
##
filesize = int(filesize)

if filesize < 1024:
  return '1 K'
elif filesize > 1048576:
  return '%s M' % (filesize/1048576)
elif filesize > 1024 and filesize < 1048576:
  return '%s K' % (filesize/1024)
