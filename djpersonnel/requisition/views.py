from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404

from djpersonnel.requisition.models import Operation
from djpersonnel.requisition.forms import OperationForm

from djzbar.decorators.auth import portal_auth_required
from djzbar.utils.hr import get_position
from djtools.utils.mail import send_mail
from djauth.LDAPManager import LDAPManager


@portal_auth_required(
    session_var='DJPERSONNEL_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def form_home(request):

    if request.method=='POST':

        form = OperationForm(
            data=request.POST, files=request.FILES, label_suffix=''
        )
        if form.is_valid():

            user = request.user
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

            # send email a creator and approver or display it for dev
            template = 'requisition/email/approver.html'
            if not settings.DEBUG:

                # send confirmation email to user who submitted the form
                to_list = [data.created_by.email,]
                bcc = [settings.ADMINS[0][1],]
                # subject
                subject = "[PRF Submission] {}, {}".format(
                    data.created_by.last_name, data.created_by.first_name
                )
                template = 'requisition/email/created_by.html'
                send_mail(
                    request, to_list, subject, settings.PRF_EMAIL_LIST[0],
                    template, data, bcc
                )

                # send email to level3 approver
                template = 'requisition/email/approver.html'
                to_list = [level3.email,]

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
        form = OperationForm(label_suffix='')

    return render(
        request, 'requisition/form_bootstrap.html', {'form': form,}
    )


@portal_auth_required(
    session_var='DJPERSONNEL_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def detail(request, rid):
    data = get_object_or_404(Operation, id=rid)
    user = request.user
    perms = data.permissions(user)
    if not perms['view']:
        raise Http404

    return render(
        request, 'requisition/detail.html', {'data':data}
    )


@portal_auth_required(
    group = settings.HR_GROUP,
    session_var='DJPERSONNEL_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def delete(request, rid):
    obj = get_object_or_404(Operation, id=rid)
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


@portal_auth_required(
    session_var='DJPERSONNEL_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def update(request, pid):
    return render(
        request, 'requisition/update.html', {}
    )
