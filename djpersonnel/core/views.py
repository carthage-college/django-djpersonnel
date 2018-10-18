# -*- coding: utf-8 -*-
from django.conf import settings
from django.apps import apps
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404

from djpersonnel.requisition.models import Operation as Requisition
from djpersonnel.transaction.models import Operation as Transaction
from djpersonnel.core.forms import DateCreatedForm
from djpersonnel.core.utils import LEVEL2

from djzbar.decorators.auth import portal_auth_required
from djtools.utils.users import in_group
from djtools.utils.mail import send_mail


@portal_auth_required(
    session_var='DJVISION_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def home(request):
    """
    dashboard home page view
    """

    user = request.user
    hr = in_group(user, settings.HR_GROUP)
    # HR or VPFA can access all objects
    if hr or user.id == LEVEL2.id:
        requisitions = Requisition.objects.all().order_by('-created_at')[:10]
        transactions = Transaction.objects.all().order_by('-created_at')[:10]
    else:
        requisitions = Requisition.objects.filter(
            Q(created_by=user) | Q(level3_approver=user)
        ).order_by('-created_at')[:10]
        transactions = Transaction.objects.filter(
            Q(created_by=user) | Q(level3_approver=user)
        ).order_by('-created_at')[:10]

    return render(
        request, 'home.html', {
            'hr':hr, 'requisitions':requisitions, 'transactions':transactions
        }
    )


@portal_auth_required(
    session_var='DJVISION_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def list(request, mod):
    """
    complete listing of all objects
    """

    user = request.user
    hr = in_group(user, settings.HR_GROUP)
    # HR or VPFA can access all objects
    if hr or user.id == LEVEL2.id:
        if mod == 'requisition':
            objects = Requisition.objects.all()
        elif mod == 'transaction':
            objects = Transaction.objects.all()
        else:
            objects = None
    else:
        if mod == 'requisition':
            objects = Requisition.objects.filter(
                Q(created_by=user) | Q(level3_approver=user)
            )
        elif mod == 'transaction':
            objects = Transaction.objects.filter(
                Q(created_by=user) | Q(level3_approver=user)
            )
        else:
            objects = None

    return render(
        request, 'list.html', {
            'hr': hr, 'objects': objects, 'mod':mod
        }
    )


@portal_auth_required(
    session_var='DJVISION_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def search(request):
    error = None
    objects = None
    if request.method == 'POST':
        form = DateCreatedForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            objects = Transaction.objects.filter(
                created_at__gte=data['created_at']
            ).all()
    else:
        form = DateCreatedForm()

    return render(
        request, 'search.html', {
            'form':form, 'objects':objects, 'error':error
        }
    )


@csrf_exempt
@portal_auth_required(
    session_var='DJVISION_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def operation_status(request):
    '''
    scope:    set the status on a operation
    options:  approve, decline
    method:   AJAX POST
    '''

    # requires POST request
    if request.POST:
        user = request.user
        oid = request.POST.get('oid')
        app = request.POST.get('app')
        model = apps.get_model(app_label=app, model_name='Operation')
        status = request.POST.get('status')
        obj = get_object_or_404(model, id=oid)
        perms = obj.permissions(user)
        if not obj.declined:
            if perms['approver'] and status in ['approved','declined']:

                from djtools.fields import NOW

                to_approver = []
                if perms['level1']:
                    level = 'level1'
                elif perms['level2']:
                    level = 'level2'
                    users = User.objects.filter(groups__name=settings.HR_GROUP)
                    for u in users:
                        to_approver.append(u.email)
                elif perms['level3']:
                    level = 'level3'
                    to_approver = [LEVEL2.email,]

                if status == 'approved':
                    setattr(obj, level, True)
                    setattr(obj, '{}_date'.format(level), NOW)

                if status == 'declined':
                    obj.declined = True

                obj.save()

                bcc = settings.MANAGERS
                frum = user.email
                to_creator = [obj.created_by.email,]
                subject = "[Personnel {} Form] {}: '{}'".format(
                    app.capitalize(), status, obj.position_title
                )
                template = '{}/email/{}_{}.html'.format(app, level, status)

                if settings.DEBUG:
                    obj.to_creator = to_creator
                    to_creator = [settings.MANAGERS[0][1],]
                    if to_approver:
                        obj.to_approver = to_approver
                        to_approver = [settings.MANAGERS[0][1],]

                # notify the creator of current status
                send_mail(
                    request, to_creator, subject, frum, template, obj, bcc
                )

                # notify the next approver
                if to_approver and status == 'approved':
                    send_mail(
                        request, to_approver, subject, frum,
                        '{}/email/approver.html'.format(app), obj, bcc
                    )

                message = "Personnel {} has been {}".format(app, status)
            else:
                message = "Access Denied"
        else:
            message = "Personnel {} has already been declined".format(app)
    else:
        message = "Requires HTTP POST"

    return HttpResponse(message)
