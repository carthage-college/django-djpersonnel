from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render

from djpersonnel.requisition.forms import OperationForm

from djzbar.decorators.auth import portal_auth_required
from djtools.utils.mail import send_mail


#@portal_auth_required(
    #session_var='DJPERSONNEL_AUTH',
    #redirect_url=reverse_lazy('access_denied')
#)
def form_home(request):
    if settings.DEBUG:
        TO_LIST = [settings.SERVER_EMAIL,]
    else:
        TO_LIST = [settings.PRF_EMAIL_LIST,]
    BCC = settings.MANAGERS

    if request.method=='POST':
        form = OperationForm(request.POST)
        if form.is_valid():
            data = form.save()
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
        form = OperationForm()

    return render(
        request, 'requisition/form_bootstrap.html', {'form': form,}
    )
