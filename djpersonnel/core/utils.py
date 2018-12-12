from django.conf import settings
from django.contrib.auth.models import Group, User

from djzbar.utils.informix import do_sql
from djzbar.utils.hr import get_position
from djzbar.utils.hr import get_cid
from djtools.utils.users import in_group

LEVEL2 = get_position(settings.LEVEL2_TPOS)
PROVOST = get_position(settings.PROVOST_TPOS)


def level3_choices():

    choices = [('','---select---')]
    level3 = settings.LEVEL3_GROUP
    for u in User.objects.filter(groups__name=level3).order_by('last_name'):
        name = '{}, {}'.format(u.last_name, u.first_name)
        choices.append((str(u.id), name))
    return choices


def get_deans():

    cids = []
    for tpos in settings.DEANS_TPOS:
        cids.append(get_position(tpos).id)
    return cids


def get_permissions(obj, user):

    perms = {
        'view':False,'approver':False,'provost':False,
        'level3': False, 'level2': False, 'level1': False
    }

    # in_group includes an exception for superusers
    group = in_group(user, settings.HR_GROUP)
    if group:
        perms['view'] = True
        perms['approver'] = True
        perms['level1'] = True
    elif user.id == PROVOST.id:
        perms['view'] = True
        perms['approver'] = True
        perms['provost'] = True
    elif user.id == LEVEL2.id:
        perms['view'] = True
        if obj.notify_level2():
            perms['approver'] = True
            perms['level2'] = True
    elif obj.level3_approver == user:
        perms['view'] = True
        perms['approver'] = True
        perms['level3'] = True
    elif obj.created_by == user:
        perms['view'] = True

    return perms
