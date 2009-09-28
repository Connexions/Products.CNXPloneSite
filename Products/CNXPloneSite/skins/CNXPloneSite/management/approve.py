# Approve accounts specified in selected fields

ids = context.REQUEST.get('ids', [])
template = context.REQUEST.get('emailBody','')

users = map(context.portal_membership.getMemberById, ids)
for u in users:
    context.portal_membership.setMemberProperties(u, status='Approved',
                                                  approved_time=DateTime())
    # FIXME: This is GRUF specific, but it's so nice to have....
    context.acl_users.changeUser(u.getId(), roles=['Member'])
    if context.REQUEST.has_key('email'):
        body = template % u.getUserName()
        context.sendEmail(messageText=body, mto=u.getProperty('email'), mfrom='cnx@rice.edu', subject='Connexions Account Approved')

psm = context.translate("message_accounts_approved", domain="rhaptos", default="Accounts approved")
context.REQUEST.RESPONSE.redirect("pending_accounts?portal_status_message="+psm)
