# -*- coding: utf-8 -*-

import argparse
import datetime
import django
import logging
import sys


django.setup()


from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import User
from djpersonnel.core.utils import get_level2
from djpersonnel.core.utils import get_deans
from djpersonnel.core.utils import get_provost
from djpersonnel.requisition.models import Operation as Requisition
from djpersonnel.transaction.models import Operation as Transaction
from djtools.utils.mail import send_mail
from djtools.utils.users import in_group


logger = logging.getLogger('debug_logfile')

# set up command-line options
desc = """
Accepts as input app name, object id, object status
"""

# RawTextHelpFormatter method allows for new lines in help text
parser = argparse.ArgumentParser(
    description=desc, formatter_class=argparse.RawTextHelpFormatter
)

parser.add_argument(
    '-a', '--app',
    required=True,
    help="App name (e.g. transaction).",
    dest='app'
)
parser.add_argument(
    '-c', '--cid',
    required=True,
    help="College ID (e.g. 8675309).",
    dest='cid'
)
parser.add_argument(
    '-o', '--oid',
    required=True,
    help="object ID.",
    dest='oid'
)
parser.add_argument(
    '-s', '--status',
    required=True,
    help="Object status (e.g. approved).",
    dest='status'
)


LEVEL2 = get_level2()
PROVOST = get_provost()


def main():
    """test status operations"""
    message = None
    user = User.objects.get(pk=cid)
    model = apps.get_model(app_label=app, model_name='Operation')

    print(app)
    print(cid)
    print(model)
    print(oid)
    print(status)
    print(user)

    hr = in_group(user, settings.HR_GROUP)
    manager = in_group(user, settings.MANAGER_GROUP)
    print(hr)
    print(manager)
    print(LEVEL2)
    try:
        obj = model.objects.get(pk=oid)
    except Exception:
        message = 'no object found with id {0}'.format(oid)

    if obj and not obj.declined:
        perms = obj.permissions(user)
        print(perms)
        '''
        # we verify that the user has permission to approve/decline
        # in the permissions method
        if perms['approver'] and status in ['approved', 'declined']:
            now = datetime.datetime.now()
            if status == 'approved':
                for level in perms['level']:
                    setattr(obj, level, True)
                    setattr(obj, '{0}_date'.format(level), now)
            if status == 'declined':
                obj.declined = True
                if app == 'budget':
                    obj.declined_date = now
            obj.save()
            message = "{0} has been {1}".format(app, status)
            if app != 'budget':
                # we will always use the first level in the list unless:
                # 1. VPFA is a level3 approver; or
                # 2. provost is a level3 approver and PAF from faculty
                # 3. HR is a level3 approver and no budget impact
                try:
                    level = perms['level'][1]
                except:
                    level = perms['level'][0]
                template = '{0}/email/{1}_{2}.html'.format(app, level, status)
                # we send an email to Level2 if money is involved
                # and then to HR for final decision. if no money, we send an
                # email to Provost if need be and then to HR for final approval.
                #
                # VPFA will be notified only if the submission does not impact
                # the budget and she is not the level3 approver.
                # at the moment, the VPFA is not a LEVEL3 approver
                # so that last AND clause in elif will never be True but LEVEL2
                # might become a LEVEL3 approver in the future
                if app != 'requisition' and obj.notify_provost() and not obj.provost:
                    to_approver = [PROVOST.email]
                elif obj.notify_level2() and not obj.level2 and obj.level3_approver.id != LEVEL2.id:
                    to_approver = [LEVEL2.email]
                else:
                    to_approver = settings.ACCOUNTING_EMAIL
                    to_approver.append(settings.HR_EMAIL)
                logger.debug('to_approver = {0}'.format(to_approver))
                bcc = [settings.ADMINS[0][1]]
                frum = user.email
                to_creator = [obj.created_by.email]
                subject = "[Personnel {0} Form] {1}".format(
                    app.capitalize(), status,
                )
                # add HR email if approved
                if obj.approved() and status == 'approved':
                    to_creator.append(settings.HR_EMAIL)
                if settings.DEBUG:
                    obj.to_creator = to_creator
                    to_creator = [settings.MANAGERS[0][1]]
                    obj.to_approver = to_approver
                    to_approver = [settings.MANAGERS[0][1], 'skirk@carthage.edu']
                # notify the creator of current status
                sent = send_mail(
                    request,
                    to_creator,
                    subject,
                    frum,
                    template,
                    obj,
                    reply_to=[frum,],
                    bcc=bcc,
                )
                # notify the next approver if it is not completely approved
                # and the submission has not been declined
                if not obj.approved() and status == 'approved':
                    send_mail(
                        request,
                        to_approver,
                        subject,
                        frum,
                        '{0}/email/approver.html'.format(app),
                        obj,
                        reply_to=[frum,],
                        bcc=bcc,
                    )
        else:
            message = "Access Denied"
        '''
    else:
        if not message:
            message = "{0} has already been declined".format(app)

    print(message)


if __name__ == '__main__':
    args = parser.parse_args()
    app = args.app
    cid = args.cid
    oid = args.oid
    status = args.status
    sys.exit(main())
