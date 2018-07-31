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
    if settings.DEBUG:
        TO_LIST = [settings.SERVER_EMAIL,]
    else:
        TO_LIST = [settings.PRF_EMAIL_LIST,]
    BCC = settings.MANAGERS

    if request.method=='POST':
        form = OperationForm(request.POST, label_suffix='')
        if form.is_valid():
            data = form.save(commit=False)
            user = request.user
            data.created_by = user
            data.updated_by = user
            data.save()
            email = data.created_by.email
            subject = "[PRF Submission] {}, {}".format(
                data.created_by.last_name, data.created_by.first_name
            )
            send_mail(
                request, TO_LIST, subject, email,'requisition/email.html',
                data, BCC
            )
            return HttpResponseRedirect(
                reverse_lazy('requisition_form_success')
            )
    else:
        form = OperationForm(label_suffix='')

    return render(
        request, 'requisition/form_bootstrap.html', {'form': form,}
        #request, 'requisition/form.html', {'form': form,}
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

