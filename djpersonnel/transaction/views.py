# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse_lazy
from djauth.decorators import portal_auth_required
from djpersonnel.transaction.models import Operation
from djpersonnel.transaction.forms import OperationForm
from djtools.utils.mail import send_mail
from djtools.utils.users import in_group


@portal_auth_required(
    session_var='DJPERSONNEL_AUTH',
    redirect_url=reverse_lazy('access_denied'),
)
def form_home(request):
    """Submit a PAF."""
    user = request.user
    if request.method=='POST':

        p = request.POST
        form = OperationForm(request.POST, label_suffix='')
        if form.is_valid():
            paf = form.save(commit=False)
            # deal with level 3 approver
            level3 = User.objects.get(username=form.cleaned_data['approver'])
            paf.created_by = user
            paf.updated_by = user
            paf.level3_approver = level3
            paf.save()

            # send email or display it for dev
            if not settings.DEBUG:

                # email distribution list and bcc parameters
                bcc = [settings.ADMINS[0][1], settings.HR_EMAIL]
                # send confirmation email to user who submitted the form
                to_list = [paf.created_by.email]
                template = 'transaction/email/created_by.html'
                # subject
                subject = "[PAF Submission] {0}, {1}".format(
                    paf.created_by.last_name, paf.created_by.first_name,
                )
                send_mail(
                    request,
                    to_list,
                    subject,
                    settings.HR_EMAIL,
                    template,
                    paf,
                    bcc,
                )
                # send email to level3 approver
                template = 'transaction/email/approver.html'
                to_list = [level3.email]
                send_mail(
                    request,
                    to_list,
                    subject,
                    paf.created_by.email,
                    template,
                    paf,
                    bcc,
                )

                return HttpResponseRedirect(
                    reverse_lazy('transaction_form_success'),
                )
            else:
                # display the email template
                template = 'transaction/email/approver.html'
                return render(request, template, {'paf': paf, 'form': form})
    else:
        form = OperationForm(label_suffix='')

    hr = in_group(user, settings.HR_GROUP)
    return render(
        request, 'transaction/form.html', {'form': form,'hr':hr}
    )


@portal_auth_required(
    session_var='DJPERSONNEL_AUTH',
    redirect_url=reverse_lazy('access_denied'),
)
def detail(request, tid):
    """Display a PAF."""
    paf = get_object_or_404(Operation, pk=tid)
    user = request.user
    perms = paf.permissions(user)

    if not perms['view']:
        raise Http404

    hr = in_group(user, settings.HR_GROUP)
    return render(
        request,
        'transaction/detail.html',
        {'hr': hr, 'data': paf, 'perms': perms},
    )


@portal_auth_required(
    group = settings.HR_GROUP,
    session_var='DJPERSONNEL_AUTH',
    redirect_url=reverse_lazy('access_denied'),
)
def delete(request, tid):
    """Delete a PAF."""
    paf = get_object_or_404(Operation, pk=tid)
    title = paf.position_title
    paf.delete()
    messages.add_message(
        request,
        messages.SUCCESS,
        "PAF {0} was deleted.".format(title),
        extra_tags='alert-success',
    )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@portal_auth_required(
    session_var='DJPERSONNEL_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def update(request, tid):
    """Update a PAF."""
    return render(request, 'transaction/update.html', {})


@portal_auth_required(
    group = settings.HR_GROUP,
    session_var='DJPERSONNEL_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def appointment_letter(request, tid):
    """Display the appointment letter."""
    paf = get_object_or_404(Operation, pk=tid)
    return render(
        request, 'transaction/appointment_letter.html', {'paf': paf},
    )


@portal_auth_required(
    group = settings.HR_GROUP,
    session_var='DJPERSONNEL_AUTH',
    redirect_url=reverse_lazy('access_denied'),
)
def graduate_assistant_letter(request, tid):
    """Display the graduate assistant letter."""
    paf = get_object_or_404(Operation, pk=tid)
    return render(
        request, 'transaction/graduate_assistant_letter.html', {'paf': paf},
    )
