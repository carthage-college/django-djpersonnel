from django.conf import settings

from djzbar.utils.informix import do_sql
from djzbar.utils.hr import get_position

from djtools.utils.users import in_group

from djpersonnel.core.sql import LEVEL3

LEVEL2 = get_position(settings.LEVEL2_TPOS)


def level3_choices():

    level3 = do_sql(LEVEL3S)
    choices = [('','---select---')]

    if level3:
        for l in level3:
            name = '{}, {}'.format(l.lastname, l.firstname)
            choices.append((str(l.id), name))
    else:
        choices = None
    return choices


def get_permissions(obj, user):

    perms = {
        'view':False,'approver':False,
        'level3': False, 'level2': False, 'level1': False
    }

    # in_group includes an exception for superusers
    group = in_group(user, settings.HR_GROUP)
    if group:
        perms['view'] = True
        perms['approver'] = True
        perms['level1'] = True
    elif user.id == LEVEL2.id:
        perms['view'] = True
        if obj.notify_veep():
            perms['approver'] = True
            perms['level2'] = True
    elif obj.level3_approver == user:
        perms['view'] = True
        perms['approver'] = True
        perms['level3'] = True
    elif obj.created_by == user:
        perms['view'] = True

    return perms
