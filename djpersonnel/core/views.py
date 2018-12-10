# -*- coding: utf-8 -*-
from django.conf import settings
from django.apps import apps
from django.db.models import Q
from django.core import serializers
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import Group, User
from django.core.urlresolvers import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from djpersonnel.requisition.models import Operation as Requisition
from djpersonnel.transaction.models import Operation as Transaction
from djpersonnel.core.forms import ApproverForm, DateCreatedForm
from djpersonnel.core.utils import LEVEL2

from djzbar.decorators.auth import portal_auth_required
from djtools.utils.convert import str_to_class
from djtools.utils.users import in_group
from djtools.utils.mail import send_mail
from djzbar.utils.hr import get_cid

from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook


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
    group = settings.HR_GROUP,
    session_var='DJVISION_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def approver_manager(request):
    user = None
    level3 = settings.LEVEL3_GROUP
    message = None
    banner = messages.SUCCESS
    tag = 'alert-success'
    hr = in_group(user, settings.HR_GROUP)

    if request.method == 'POST':
        form = ApproverForm(
            request.POST, use_required_attribute=settings.REQUIRED_ATTRIBUTE
        )
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                if in_group(user, level3):
                    form.add_error(
                        'email', "{}, {} is already in the Approvers group".format(
                            user.last_name, user.first_name
                        )
                    )
                    message = "User is already in the Approvers group"
                    banner = messages.ERROR
                    tag = 'alert-danger'
                else:
                    message = "{}, {} added to the Approvers group".format(
                        user.last_name, user.first_name
                    )
                    form = ApproverForm(
                        use_required_attribute=settings.REQUIRED_ATTRIBUTE
                    )
            except:
                cid = get_cid(email)
                if cid:
                    user = form.save(commit=False)
                    user.username = user.email.split('@')[0]
                    user.id = cid
                    user.set_password(
                        User.objects.make_random_password(length=24)
                    )
                    user.save()
                    message = "{}, {} added to the Approvers group".format(
                        user.last_name, user.first_name
                    )
                    form = ApproverForm(
                        use_required_attribute=settings.REQUIRED_ATTRIBUTE
                    )
                else:
                    form.add_error(
                        'email', "There is no user with that email address"
                    )
                    message = "There is no user with that email address"
                    banner = messages.ERROR
                    tag = 'alert-danger'
            if user:
                group = Group.objects.get(name=level3)
                group.user_set.add(user)
            if message:
                messages.add_message(
                    request, banner, message, extra_tags=tag
                )
    else:
        form = ApproverForm(use_required_attribute=settings.REQUIRED_ATTRIBUTE)

    objects = User.objects.filter(groups__name=level3).order_by('last_name')

    return render(
        request, 'approver.html', {'hr': hr, 'form':form, 'objects':objects}
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
                # we send an email to Level2 if money is involved
                # and then to HR for final decision. if no money, we send
                # an email to HR for final decision.
                hr_group = []
                to_approver = []
                for u in User.objects.filter(groups__name=settings.HR_GROUP):
                    hr_group.append(u.email)

                if perms['level1']:
                    level = 'level1'
                elif perms['level2']:
                    level = 'level2'
                    to_approver = hr_group
                elif perms['level3']:
                    level = 'level3'
                    if not obj.notify_veep:
                        to_approver = hr_group
                    else:
                        to_approver = [LEVEL2.email,]

                if status == 'approved':
                    setattr(obj, level, True)
                    setattr(obj, '{}_date'.format(level), NOW)

                if status == 'declined':
                    obj.declined = True

                obj.save()

                bcc = [settings.ADMINS[0][1],]
                frum = user.email
                to_creator = [obj.created_by.email,]
                subject = "[Personnel {} Form] {}".format(
                    app.capitalize(), status
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

                # notify the next approver if we have one and the submission
                # has not been declined
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


def openxml(request, mod):

    wb = Workbook()
    ws = wb.get_active_sheet()

    model = str_to_class(
        'djpersonnel.{}.models'.format(mod), 'Operation'
    )

    data = serializers.serialize('python', model.objects.all() )

    head = False
    headers = []
    for d in data:
        row = []
        for n,v in d['fields'].items():
            headers.append(model._meta.get_field(n).verbose_name.title())
            row.append(v)
        if not head:
            ws.append(headers)
            head = True
        ws.append(row)

    response = HttpResponse(
        save_virtual_workbook(wb), content_type='application/ms-excel'
    )

    response['Content-Disposition'] = 'attachment;filename={}.xlsx'.format(
        mod
    )

    return response
