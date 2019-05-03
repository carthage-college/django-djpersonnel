from django.conf import settings
from django.contrib.auth.models import Group, User

from djzbar.utils.hr import get_position
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
        'view':False,'approver':False,'provost':False,'level':[]
    }

    # in_group includes an exception for superusers
    group = in_group(user, settings.HR_GROUP)
    # Level 3 approver might also be in the HR group, in which case
    # she will approve at level 3 first, then VPFA approves, then she will
    # approve once again as HR, unless the request does not involve the
    # VPFA (no budget impact), then she will approve level3 and level1
    # all in one go.
    if group and obj.level3_approver == user and not obj.level3:
        perms['view'] = True
        perms['approver'] = True
        perms['level'].append('level3')
        if not obj.notify_level2():
            perms['level'].append('level1')
    # the rest of HR
    elif group:
        perms['view'] = True
        perms['approver'] = True
        perms['level'].append('level1')
    # Provost (does not approve any submissions: is notified, and can view)
    elif user.id == PROVOST.id:
        perms['view'] = True
        perms['provost'] = True
    # VPFA might also be a level 3 approver, but does not approve submissions
    # that do not impact the budget
    elif user.id == LEVEL2.id:
        perms['view'] = True
        if obj.level3_approver == user:
            perms['level'].append('level3')
        # money involved
        if obj.notify_level2():
            perms['approver'] = True
            perms['level'].append('level2')
    # VP/Dean approver
    elif obj.level3_approver == user:
        perms['view'] = True
        perms['approver'] = True
        perms['level'].append('level3')
    elif obj.created_by == user:
        perms['view'] = True

    return perms
