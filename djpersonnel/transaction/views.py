from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, get_object_or_404

from djpersonnel.transaction.models import Operation
from djpersonnel.transaction.forms import OperationForm

from djzbar.decorators.auth import portal_auth_required
from djzbar.utils.hr import get_position
from djauth.LDAPManager import LDAPManager
from djtools.utils.mail import send_mail
from djtools.utils.users import in_group


@portal_auth_required(
    session_var='DJPERSONNEL_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def form_home(request):
    user = request.user
    switch = request.GET.get('switch')
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
                bcc = [settings.ADMINS[0][1],]
                # send confirmation email to user who submitted the form
                to_list = [data.created_by.email,]
                template = 'transaction/email/created_by.html'
                # subject
                subject = u"[PAF Submission] {}, {}".format(
                    data.created_by.last_name, data.created_by.first_name
                )
                send_mail(
                    request, to_list, subject, settings.PAF_EMAIL_LIST[0],
                    template, data, bcc
                )

                # send approver email to VP or Provost
                template = 'transaction/email/approver.html'
                send_mail(
                    request, [data.level3_approver.email,], subject,
                    data.created_by.email, template, data, bcc
                )

                return HttpResponseRedirect(
                    reverse_lazy('transaction_form_success')
                )
            else:
                # display the email template
                template = 'transaction/email/approver.html'
                #template = 'transaction/email/created_by.html'
                return render(
                    request, template, {'data': data,'form':form}
                )
    else:
        form = OperationForm(label_suffix='')

    hr = in_group(user, settings.HR_GROUP)

    template = 'transaction/form.html'
    if switch:
        template = 'transaction/form_{}.html'.format(switch)

    return render(
        request, template, {'form': form,'hr':hr,'switch':switch}
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

    return render(
        request, 'transaction/detail.html', {'data':data,'perms':perms}
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

