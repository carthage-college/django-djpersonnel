from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404

from djpersonnel.requisition.models import Operation
from djpersonnel.requisition.forms import OperationForm
from djpersonnel.core.utils import PROVOST

from djimix.decorators.auth import portal_auth_required
from djtools.utils.mail import send_mail
from djtools.utils.users import in_group
from djauth.LDAPManager import LDAPManager


@portal_auth_required(
    session_var='DJPERSONNEL_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
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
            data=request.POST,instance=obj,files=request.FILES,label_suffix='',
            use_required_attribute=False
        )
        if form.is_valid():
            data = form.save(commit=False)
            data.created_by = user
            data.updated_by = user
            data.save()

            # send email to creator and approver or display it for dev,
            # and do not send it if we are updating the object
            template = 'requisition/email/approver.html'
            if not settings.DEBUG and not obj:

                # send confirmation email to user who submitted the form
                to_list = [data.created_by.email]
                bcc = [settings.ADMINS[0][1], settings.HR_EMAIL]
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
                to_list = [data.level3_approver.email,]
                if data.notify_provost():
                    to_list.append(PROVOST.email)
                send_mail(
                    request, to_list, subject, data.created_by.email,
                    template, data, bcc
                )

                return HttpResponseRedirect(
                    reverse_lazy('requisition_form_success')
                )
            else:
                # display the email template
                return render(
                    request, template, {'data': data,'form':form}
                )
    else:
        form = OperationForm(instance=obj,label_suffix='',use_required_attribute=False)

    hr = in_group(user, settings.HR_GROUP)
    return render(
        request,'requisition/form.html',{'hr':hr, 'form': form,}
    )


@portal_auth_required(
    session_var='DJPERSONNEL_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def detail(request, rid):
    data = get_object_or_404(Operation, pk=rid)
    user = request.user
    perms = data.permissions(user)
    if not perms['view']:
        raise Http404

    hr = in_group(user, settings.HR_GROUP)
    return render(
        request, 'requisition/detail.html', {'hr':hr,'data':data,'perms':perms}
    )


@portal_auth_required(
    group = settings.HR_GROUP,
    session_var='DJPERSONNEL_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def delete(request, rid):
    obj = get_object_or_404(Operation, pk=rid)
    title = obj.position_title
    obj.delete()

    messages.add_message(
        request, messages.SUCCESS, "PRF {} was deleted.".format(title),
        extra_tags='alert-success'
    )

    # there is no referer in unit tests
    redirect = request.META.get('HTTP_REFERER')
    if not redirect:
        redirect = reverse_lazy('dashboard_home')

    return HttpResponseRedirect(redirect)

