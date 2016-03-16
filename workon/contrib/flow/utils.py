
# encoding: utf-8



# def send_staff_notification(title, body=None,
#     send_emails=True,
#     email_title_prefix="[STAFF] ",
#     email_layout="django_flow/admin/email/base.html",
#     email_sender=conf.settings.DEFAULT_NO_REPLY_EMAIL,
#     email_receivers=[],
#     email_context={}):

#     StaffNotification.objects.create(
#         title=title,
#         body=body,
#     )

#     if not email_receivers:
#         email_receivers = conf.settings.STAFF_EMAILS.values()

#     send_template_email(
#         u'%s%s' % (email_title_prefix, title),
#         email_sender,
#         email_receivers,
#         template="django_flow/admin/email/staff_notification.html",
#         context= {
#             'layout': email_layout,
#             'title': title,
#             'body': body,
#         }
#     )
