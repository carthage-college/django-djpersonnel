# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from djtools.utils.users import in_group
from djtools.utils.workday import get_managers


def level3_choices():
    """Obtain the folks who will approve the request at level 3."""
    choices = [('','---select---')]
    level3 = settings.LEVEL3_GROUP
    for user in User.objects.filter(groups__name=level3).order_by('last_name'):
        name = '{0}, {1}'.format(user.last_name, user.first_name)
        choices.append((str(user.username), name))
    return choices


def get_deans():
    """Obtain the deans."""
    cids = []
    for dean in get_managers('deans'):
        cids.append(dean['id'])
    return cids


def get_provost():
    """Obtain the provost."""
    return User.objects.filter(groups__name=settings.PROVOST_GROUP).first()


def get_level2():
    """Obtain the provost."""
    return User.objects.filter(groups__name=settings.LEVEL2_GROUP).first()


def get_permissions(obj, user):
    """Establish permissions for a user on the object."""
    perms = {'view': False, 'approver': False, 'provost': False, 'level': []}
    # in_group includes an exception for superusers
    hr = in_group(user, settings.HR_GROUP)
    manager = in_group(user, settings.MANAGER_GROUP)
    # Level 3 approver might also be in the HR group, in which case
    # she will approve at level 3 first, then VPFA approves, then she will
    # approve once again as HR, unless the request does not involve the
    # VPFA (no budget impact), then she will approve level3 and level1
    # all in one go.
    if hr and obj.level3_approver == user and not obj.level3:
        perms['view'] = True
        perms['approver'] = True
        perms['level'].append('level3')
        if not obj.notify_level2():
            perms['level'].append('level1')
    # the rest of HR
    elif hr:
        perms['view'] = True
        perms['approver'] = True
        perms['level'].append('level1')
    elif manager:
        perms['view'] = True
    # Provost:
    #   1) approves PAF for faculty submissions only (not PRF...for now)
    #   2) will be an approver for level3 or provost but not both
    #   3) provost level is between levels 3 and 2
    elif user.id == get_provost().id:
        perms['view'] = True
        if obj._meta.verbose_name.title() == "Transaction":
            perms['approver'] = True
            perms['provost'] = True
            perms['level'].append('provost')
        # provost can also be a level3 approver on both
        # Transaction and Requisition
        if obj.level3_approver == user:
            perms['approver'] = True
            perms['level'].append('level3')
    # VPFA might also be a level 3 approver, but does not approve submissions
    # that do not impact the budget
    elif user.id == get_level2().id:
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
