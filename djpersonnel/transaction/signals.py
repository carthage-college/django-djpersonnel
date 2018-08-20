from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from djpersonnel.transaction.models import Operation
from djtools.utils.mail import send_mail



@receiver(post_save, sender=Operation)
def transaction_operation_post_save_notify_hr(sender, **kwargs):
    """
    send an email to HR when all approvals for a transaction operation
    have been met
    """

    obj = kwargs['instance']

    '''
    if not obj.decline and obj.step1() and obj.step2() \
    and not obj.email_approved:

        to_list = [settings.PROPOSAL_EMAIL,]
        if settings.DEBUG:
            obj.to_list = to_list
            to_list = [settings.MANAGERS[0][1],]

        # send the email OSP
        subject = "[Final] Proposal approved: '{}' by {}, {}".format(
            obj.title, obj.user.last_name, obj.user.first_name
        )
        sent = send_mail(
            kwargs.get('request'), to_list,
            subject, settings.SERVER_MAIL,
            'proposal/email_final_approved.html', obj, settings.MANAGERS
        )
        if sent:
            obj.email_approved = True
            obj.save()
    '''
