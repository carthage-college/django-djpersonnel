from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, get_object_or_404

from djpersonnel.transaction.models import Operation
from djpersonnel.transaction.forms import OperationForm

from djtools.utils.mail import send_mail

from djzbar.decorators.auth import portal_auth_required


#@portal_auth_required(
    #session_var='DJPERSONNEL_AUTH',
    #redirect_url=reverse_lazy('access_denied')
#)
def form_home(request):
    if settings.DEBUG:
        TO_LIST = [settings.SERVER_EMAIL,]
    else:
        TO_LIST = [settings.PAF_EMAIL_LIST,]
    BCC = settings.MANAGERS

    if request.method=='POST':
        form = OperationForm(request.POST)
        if form.is_valid():
            data = form.save()
            email = data.created_by.email
            subject = "[PAF Submission] {}, {}".format(
                data.created_by.last_name, data.created_by.first_name
            )
            send_mail(
                request, TO_LIST, subject, email,'transaction/email.html',
                data, BCC
            )
            return HttpResponseRedirect(
                reverse_lazy('transaction_form_success')
            )
    else:
        form = OperationForm()

    return render(
        request, 'transaction/form.html', {'form': form,}
    )


@portal_auth_required(
    session_var='DJPERSONNEL_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def display(request, tid):
    data = get_object_or_404(Operation, id=tid)
    return render(
        request, 'transaction/display.html', {'data':data}
    )


@portal_auth_required(
    session_var='DJPERSONNEL_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def update(request, pid):
    return render(
        request, 'transaction/update.html', {}
    )
