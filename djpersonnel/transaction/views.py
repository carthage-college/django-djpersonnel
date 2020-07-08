from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404

from djpersonnel.transaction.models import Operation
from djpersonnel.transaction.forms import OperationForm

from djimix.decorators.auth import portal_auth_required
from djauth.LDAPManager import LDAPManager
from djtools.utils.mail import send_mail
from djtools.utils.users import in_group


@portal_auth_required(
    session_var='DJPERSONNEL_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def form_home(request):
    user = request.user
    if request.method=='POST':

        p = request.POST
        form = OperationForm(request.POST, label_suffix='')
        if form.is_valid():
            # deal with level 3 approver
            lid = form.cleaned_data['approver']
            try:
                level3 = User.objects.get(pk=lid)
            except:
                l = LDAPManager()
                luser = l.search(lid)
                level3 = l.dj_create(luser)

            data = form.save(commit=False)
            data.created_by = user
            data.updated_by = user
            data.level3_approver = level3
            data.save()

            # send email or display it for dev
            if not settings.DEBUG:

                # email distribution list and bcc parameters
                bcc = [settings.ADMINS[0][1], settings.HR_EMAIL]
                # send confirmation email to user who submitted the form
                to_list = [data.created_by.email]
                template = 'transaction/email/created_by.html'
                # subject
                subject = "[PAF Submission] {0}, {1}".format(
                    data.created_by.last_name, data.created_by.first_name,
                )
                send_mail(
                    request,
                    to_list,
                    subject,
                    settings.HR_EMAIL,
                    template,
                    data,
                    bcc,
                )
                # send email to level3 approver
                template = 'transaction/email/approver.html'
                to_list = [level3.email]
                send_mail(
                    request,
                    to_list,
                    subject,
                    data.created_by.email,
                    template,
                    data,
                    bcc,
                )

                return HttpResponseRedirect(
                    reverse_lazy('transaction_form_success')
                )
            else:
                # display the email template
                template = 'transaction/email/approver.html'
                return render(
                    request, template, {'data': data,'form':form}
                )
    else:
        form = OperationForm(label_suffix='')

    hr = in_group(user, settings.HR_GROUP)
    return render(
        request, 'transaction/form.html', {'form': form,'hr':hr}
    )


@portal_auth_required(
    session_var='DJPERSONNEL_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def detail(request, tid):
    data = get_object_or_404(Operation, id=tid)
    user = request.user
    perms = data.permissions(user)

    if not perms['view']:
        raise Http404

    hr = in_group(user, settings.HR_GROUP)
    return render(
        request, 'transaction/detail.html', {'hr':hr,'data':data,'perms':perms}
    )


@portal_auth_required(
    group = settings.HR_GROUP,
    session_var='DJPERSONNEL_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def delete(request, tid):
    obj = get_object_or_404(Operation, id=tid)
    title = obj.position_title
    obj.delete()

    messages.add_message(
        request, messages.SUCCESS, "PAF {} was deleted.".format(title),
        extra_tags='alert-success'
    )

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@portal_auth_required(
    session_var='DJPERSONNEL_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def update(request, tid):
    return render(
        request, 'transaction/update.html', {}
    )


@portal_auth_required(
    group = settings.HR_GROUP,
    session_var='DJPERSONNEL_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def appointment_letter(request, tid):
    data = get_object_or_404(Operation, id=tid)
    return render(
        request, 'transaction/appointment_letter.html', {'data':data}
    )


@portal_auth_required(
    group = settings.HR_GROUP,
    session_var='DJPERSONNEL_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def graduate_assistant_letter(request, tid):
    data = get_object_or_404(Operation, id=tid)
    return render(
        request, 'transaction/graduate_assistant_letter.html', {'data':data}
    )
