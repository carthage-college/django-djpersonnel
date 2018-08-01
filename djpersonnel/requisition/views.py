from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, get_object_or_404

from djpersonnel.requisition.models import Operation
from djpersonnel.requisition.forms import OperationForm

from djzbar.decorators.auth import portal_auth_required
from djtools.utils.mail import send_mail


@portal_auth_required(
    session_var='DJPERSONNEL_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def form_home(request):

    if request.method=='POST':

        form = OperationForm(request.POST, label_suffix='')
        if form.is_valid():
            data = form.save(commit=False)
            user = request.user
            data.created_by = user
            data.updated_by = user
            data.save()
            # send email or display it for dev
            template = 'requisition/email.html',
            if not settings.DEBUG:
                # email distribution list and bcc parameters
                bcc = settings.PRF_EMAIL_LIST
                bcc.append(settings.ADMINS[0][1])
                # send confirmation email to user who submitted the form
                to_list = [data.created_by.email,]
                # subject
                subject = "[PRF Submission] {}, {}".format(
                    data.created_by.last_name, data.created_by.first_name
                )
                send_mail(
                    request,to_list,subject,bcc[0],template,data,bcc
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
def display(request, rid):
    data = get_object_or_404(Operation, id=rid)
    return render(
        request, 'requisition/display.html', {'data':data}
    )


@portal_auth_required(
    session_var='DJPERSONNEL_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def update(request, pid):
    return render(
        request, 'requisition/update.html', {}
    )
