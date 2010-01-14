## Script (Python) "validate_registration"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##bind state=state
##parameters=license='',**kw
##title=validates the Registration of a User

## CNX note: no counterpart in Plone.

if not license:
    errormsg = context.translate("message_agree_to_license_to_proceed", domain="rhaptos", default="You must agree to the license to proceed.")
    state.setError('license', errormsg)

if state.getErrors():
    psm = context.translate("message_please_correct_errors", domain="rhaptos", default="Please correct the indicated errors.")
    return state.set(status='failure', portal_status_message=psm)
else:
    psm = context.translate("message_request_submitted", domain="rhaptos", default="Request submitted.")
    return state.set(portal_status_message=psm)
