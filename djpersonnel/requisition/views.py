# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse_lazy
from djpersonnel.core.utils import get_provost
from djpersonnel.requisition.models import Operation
from djpersonnel.requisition.forms import OperationForm
from djtools.utils.mail import send_mail
from djtools.decorators.auth import group_required
from djtools.utils.users import in_group


@login_required
def form_home(request, rid=None):
    user = request.user
    obj = None
    if rid:
        obj = get_object_or_404(Operation, pk=rid)
        # only HR folks can update PRF at the moment
        if not in_group(user, settings.HR_GROUP):
            return HttpResponseRedirect(reverse_lazy('access_denied'))

    if request.method=='POST':
        form = OperationForm(
            data=request.POST,
            instance=obj,
            files=request.FILES,
            label_suffix='',
            use_required_attribute=False,
        )
        if form.is_valid():
            data = form.save(commit=False)
            data.created_by = user
            data.updated_by = user
            data.save()

            # send email to creator and approver if not update
            if not obj:
                template = 'requisition/email/approver.html'
                # send confirmation email to user who submitted the form
                to_list = [data.created_by.email]
                bcc = [settings.ADMINS[0][1], settings.HR_EMAIL]
                if settings.DEBUG:
                    data.to_list = to_list
                    to_list = bcc
                # subject
                subject = "[PRF Submission] {0}, {1}".format(
                    data.created_by.last_name, data.created_by.first_name,
                )
                template = 'requisition/email/created_by.html'
                send_mail(
                    request,
                    to_list,
                    subject,
                    settings.HR_EMAIL,
                    template,
                    data,
                    bcc,
                )
                # send email to level3 approver and Provost, if need be
                # (the latter of whom just needs notification and
                # does not approve anything
                template = 'requisition/email/approver.html'
                to_list = [data.level3_approver.email]
                if data.notify_provost():
                    to_list.append(get_provost().email)
                if settings.DEBUG:
                    data.to_list = to_list
                    to_list = bcc
                send_mail(
                    request,
                    to_list,
                    subject,
                    data.created_by.email,
                    template,
                    data,
                    bcc,
                )
                return HttpResponseRedirect(reverse_lazy('requisition_form_success'))
    else:
        form = OperationForm(
            instance=obj,
            label_suffix='',
            use_required_attribute=False,
        )

    hr = in_group(user, settings.HR_GROUP)
    return render(request, 'requisition/form.html', {'hr': hr, 'form': form})


@login_required
def detail(request, rid):
    """Display the detailed data set for this requisition."""
    data = get_object_or_404(Operation, pk=rid)
    user = request.user
    perms = data.permissions(user)
    if not perms['view']:
        raise Http404

    hr = in_group(user, settings.HR_GROUP)
    return render(
        request,
        'requisition/detail.html',
        {'hr': hr, 'data': data, 'perms': perms},
    )


@group_required(settings.HR_GROUP)
def delete(request, rid):
    """Delete an instance of the Requistion object class."""
    obj = get_object_or_404(Operation, pk=rid)
    title = obj.position_title
    obj.delete()

    messages.add_message(
        request,
        messages.SUCCESS,
        "PRF {0} was deleted.".format(title),
        extra_tags='alert-success',
    )

    # there is no referer in unit tests
    redirect = request.META.get('HTTP_REFERER')
    if not redirect:
        redirect = reverse_lazy('dashboard_home')

    return HttpResponseRedirect(redirect)
