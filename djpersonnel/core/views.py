# -*- coding: utf-8 -*-

from django.apps import apps
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.core import serializers
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from djimix.decorators.auth import portal_auth_required
from djimix.people.utils import get_cid
from djpersonnel.core.forms import ApproverForm
from djpersonnel.core.forms import DateCreatedForm
from djpersonnel.core.utils import LEVEL2
from djpersonnel.core.utils import PROVOST
from djpersonnel.core.utils import get_deans
from djpersonnel.requisition.models import Operation as Requisition
from djpersonnel.transaction.models import Operation as Transaction
from djtools.utils.convert import str_to_class
from djtools.utils.mail import send_mail
from djtools.utils.users import in_group
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook


@portal_auth_required(
    session_var='DJPERSONNEL_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def home(request):
    """Dashboard home page view."""
    deans = get_deans()
    user = request.user
    hr = in_group(user, settings.HR_GROUP)
    # HR or VPFA can access all objects
    if hr or user.id == LEVEL2.id:
        requisitions = Requisition.objects.all().order_by('-created_at')[:15]
        transactions = Transaction.objects.all().order_by('-created_at')[:15]
    elif user.id == PROVOST.id:
        # PRF
        reqs1 = Requisition.objects.filter(level3_approver__pk__in=deans)
        reqs2 = Requisition.objects.filter(level3_approver__pk=PROVOST.id)
        reqs = reqs1 | reqs2
        requisitions = reqs.order_by('-created_at')[:15]
        # PAF
        trans1 = Transaction.objects.filter(level3_approver__pk__in=deans)
        trans2 = Transaction.objects.filter(level3_approver__pk=PROVOST.id)
        trans = trans1 | trans2
        transactions = trans.order_by('-created_at')[:15]
    else:
        requisitions = Requisition.objects.filter(
            Q(created_by=user) | Q(level3_approver=user)
        ).order_by('-created_at')[:15]
        transactions = Transaction.objects.filter(
            Q(created_by=user) | Q(level3_approver=user)
        ).order_by('-created_at')[:15]

    return render(
        request, 'home.html', {
            'hr':hr, 'requisitions':requisitions, 'transactions':transactions
        }
    )


@portal_auth_required(
    session_var='DJPERSONNEL_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def list(request, mod):
    """
    complete listing of all objects
    """

    deans = get_deans()
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
    # Provost can view all objects created by Deans
    elif user.id == PROVOST.id:
        if mod == 'requisition':
            objects = Requisition.objects.filter(
                level3_approver__pk__in=deans
            ).order_by('-created_at')
        elif mod == 'transaction':
            objects = Transaction.objects.filter(
                level3_approver__pk__in=deans
            ).order_by('-created_at')
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


@csrf_exempt
@portal_auth_required(
    group = settings.HR_GROUP,
    session_var='DJPERSONNEL_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def approver_manager(request):
    """Add a level 3 approver."""
    user = None
    level3_group = settings.LEVEL3_GROUP
    message = None
    banner = messages.SUCCESS
    tag = 'alert-success'

    if request.method == 'POST':
        form = ApproverForm(
            request.POST, use_required_attribute=settings.REQUIRED_ATTRIBUTE
        )
        if form.is_valid():
            data = form.cleaned_data
            # fetch user or create one if they do not exist
            try:
                user = User.objects.get(email=data['email'])
            except:
                cid = get_cid(data['email'])
                if cid:
                    user = form.save(commit=False)
                    user.username = user.email.split('@')[0]
                    user.id = cid
                    user.set_password(
                        User.objects.make_random_password(length=24)
                    )
                    user.save()
                else:
                    form.add_error(
                        'email', "There is no user with that email address"
                    )
                    message = "There is no user with that email address"
                    banner = messages.ERROR
                    tag = 'alert-danger'

            if user:
                group = Group.objects.get(name=level3_group)
                # if we have a college ID, then we remove the user from
                # the approver group
                if request.POST.get('cid'):
                    group.user_set.remove(user)
                elif in_group(user, level3_group):
                    form.add_error(
                        'email', "{}, {} is already in the Approvers group".format(
                            user.last_name, user.first_name
                        )
                    )
                    message = "User is already in the Approvers group"
                    banner = messages.ERROR
                    tag = 'alert-danger'
                else:
                    group.user_set.add(user)
                    message = "{}, {} added to the Approvers group".format(
                        user.last_name, user.first_name
                    )
                    form = ApproverForm(
                        use_required_attribute=settings.REQUIRED_ATTRIBUTE
                    )
                group.save()

            if message:
                messages.add_message(
                    request, banner, message, extra_tags=tag
                )
    else:
        form = ApproverForm(use_required_attribute=settings.REQUIRED_ATTRIBUTE)

    if request.POST.get('cid'):
        response = HttpResponse('Success', content_type="text/plain; charset=utf-8")
    else:
        objects = User.objects.filter(groups__name=level3_group).order_by('last_name')
        hr = in_group(request.user, settings.HR_GROUP)
        response = render(
            request, 'approver.html', {'hr': hr, 'form':form, 'objects':objects}
        )
    return response


@portal_auth_required(
    session_var='DJPERSONNEL_AUTH',
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
                created_at__gte=data['created_at'],
            ).all()
    else:
        form = DateCreatedForm()

    return render(
        request, 'search.html', {
            'form': form, 'objects': objects, 'error': error,
        },
    )


@csrf_exempt
@portal_auth_required(
    session_var='DJPERSONNEL_AUTH',
    redirect_url=reverse_lazy('access_denied'),
)
def operation_status(request):
    """
    scope:    set the status on a operation
    options:  approve, decline
    method:   AJAX POST
    """
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
            # we verify that the user has permission to approve/decline
            # in the permissions method
            if perms['approver'] and status in ['approved','declined']:

                from djtools.fields import NOW
                if status == 'approved':
                    for level in perms['level']:
                        setattr(obj, level, True)
                        setattr(obj, '{}_date'.format(level), NOW)

                if status == 'declined':
                    obj.declined = True

                obj.save()

                # we will always use the first level in the list unless:
                # 1. VPFA is a level3 approver; or
                # 2. provost is a level3 approver and PAF from faculty
                # 3. HR is a level3 approver and no budget impact
                try:
                    level = perms['level'][1]
                except:
                    level = perms['level'][0]
                template = '{}/email/{}_{}.html'.format(app, level, status)

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
                    to_approver = [settings.HR_EMAIL, settings.ACCOUNTING_EMAIL]

                bcc = [settings.ADMINS[0][1]]
                frum = user.email
                to_creator = [obj.created_by.email]
                subject = "[Personnel {0} Form] {1}".format(
                    app.capitalize(), status,
                )

                if settings.DEBUG:
                    obj.to_creator = to_creator
                    to_creator = [settings.MANAGERS[0][1]]
                    obj.to_approver = to_approver
                    to_approver = [settings.MANAGERS[0][1]]

                # notify the creator of current status
                send_mail(
                    request, to_creator, subject, frum, template, obj, bcc,
                )

                # notify the next approver if it is not completely approved
                # and the submission has not been declined
                if not obj.approved() and status == 'approved':
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
