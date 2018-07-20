from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render

from djpersonnel.requisition.forms import OperationForm


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
            email = settings.DEFAULT_FROM_EMAIL
            if data.email:
                email = data.email
            subject = "[Submit] {} {}".format(
                data.user.first_name, data.user.last_name
            )
            send_mail(
                request,TO_LIST, subject, email,'transaction/email.html', data, BCC
            )
            return HttpResponseRedirect(
                reverse_lazy('transaction_success')
            )
    else:
        form = OperationForm()

    return render(
        request, 'requisition/form_bootstrap.html', {'form': form,}
    )