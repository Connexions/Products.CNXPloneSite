## Script (Python) "sendEmail"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=messageText,mto,mfrom,subject
##title=
##
# This is called out in a Python script so that it can
# have the proxy role of "manager".

# More complex version of mail call from
# http://aspn.activestate.com/ASPN/Mail/Message/zope-List/950840
# to get around "undisclosed-recipients" problem until Zope 2.4.3.

# Wait...this *is* Zope 2.4.3....

encode = None

body = "\r\n".join(["From: %s" % mfrom,
                    "To: %s" % mto,
                    "Subject: %s" % subject,
                    "",
                    messageText])

context.MailHost.send(body, mto, mfrom, subject, encode)
