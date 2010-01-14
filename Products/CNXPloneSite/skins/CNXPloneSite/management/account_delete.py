#if remove user was checked
removed = context.REQUEST.get('ids', [])

if removed:
    context.acl_users.userFolderDelUsers(removed)
    context.Members.manage_delObjects(removed)

psm = context.translate("message_accounts_deleted", domain="rhaptos", default="Accounts deleted.")
url='%s?%s' % (context.REQUEST.HTTP_REFERER, 'portal_status_message='+psm)
return context.REQUEST.RESPONSE.redirect(url)
