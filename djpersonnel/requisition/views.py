from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, Http404
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
            # deal with VP/Provost
            vpid = form.cleaned_data['veep']
            try:
                veep = User.objects.get(pk=vpid)
            except:
                l = LDAPManager()
                luser = l.search(vpid)
                veep = l.dj_create(luser)

            data = form.save(commit=False)
            data.created_by = user
            data.updated_by = user
            data.level3_approver = veep
            data.save()

            # send email or display it for dev
            #template = 'requisition/email/created_by.html'
            template = 'requisition/email/approver.html'
            if not settings.DEBUG:

                # email distribution list and bcc parameters
                bcc = [settings.ADMINS[0][1],]
                # send confirmation email to user who submitted the form
                to_list = [data.created_by.email,]
                # subject
                subject = "[PRF Submission] {}, {}".format(
                    data.created_by.last_name, data.created_by.first_name
                )

                send_mail(
                    request, to_list, subject, settings.PRF_EMAIL_LIST[0],
                    template, data, bcc
                )

                # send approver email to VP or Provost
                template = 'requisition/email/approver.html'
                # waiting for SQL that identifies staff VP
                veep = False
                if veep:
                    to_list = []
                else:
                    #to_list = [get_position(settings.PROV_TPOS).email]
                    to_list = bcc

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
    session_var='DJPERSONNEL_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def update(request, pid):
    return render(
        request, 'requisition/update.html', {}
    )
