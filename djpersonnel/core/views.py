# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404

from djpersonnel.requisition.models import Operation as Requisition
from djpersonnel.transaction.models import Operation as Transaction
from djpersonnel.core.forms import DateCreatedForm

from djzbar.decorators.auth import portal_auth_required
from djtools.utils.users import in_group


@portal_auth_required(
    group='Human Resources', session_var='DJVISION_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def home(request):
    """
    dashboard home page view
    """

    user = request.user

    group = in_group(user, settings.HR_GROUP)

    if group:
        requisitions = Requisition.objects.all()
        transactions = Transaction.objects.all()
    else:
        requisitions = Requisition.objects.filter(created_by=user)
        transactions = Transaction.objects.filter(created_by=user)

    return render(
        request, 'home.html', {
            'requisitions':requisitions, 'transactions':transactions
        }
    )


@portal_auth_required(
    group='Human Resources', session_var='DJVISION_AUTH',
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
    group='Human Resources', session_var='DJVISION_AUTH',
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
        model = request.POST.get('model')
        status = request.POST.get('status')
        obj = get_object_or_404(model, id=oid)
        perms = obj.permissions(user)

        if perms['approver']:
            if status == 'approved':
                pass
            if status == 'declined':
                pass
            message = "{} has been {}".format(model, status)
        else:
            message = "Access Denied"
    else:
        message = "Requires POST request"

    return HttpResponse(message)
