from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, get_object_or_404

from djpersonnel.paf.forms import OperationForm

from djtools.utils.mail import send_mail
from djzbar.decorators.auth import portal_auth_required


@portal_auth_required(
    session_var='DJPERSONNEL_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def form(request):
    if settings.DEBUG:
        TO_LIST = [settings.SERVER_EMAIL,]
    else:
        TO_LIST = [settings.MY_APP_EMAIL,]
    BCC = settings.MANAGERS

    if request.method=='POST':
        form_op = OperationForm(request.POST, request.FILES)
        if form_op.is_valid():
            data = form_op.save()
            email = settings.DEFAULT_FROM_EMAIL
            if data.email:
                email = data.email
            subject = "[Submit] {} {}".format(
                data.user.first_name, data.user.last_name
            )
            send_mail(
                request,TO_LIST, subject, email,'paf/email.html', data, BCC
            )
            return HttpResponseRedirect(
                reverse_lazy('paf_success')
            )
    else:
        form_op = OperationForm()

    return render(
        request, 'paf/form.html', {'form': form_op,}
    )


@portal_auth_required(
    session_var='DJPERSONNEL_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def list(request):
    return render(
        request, 'paf/list.html', {}
    )


@portal_auth_required(
    session_var='DJPERSONNEL_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def display(request, pid):
    return render(
        request, 'paf/display.html', {}
    )


@portal_auth_required(
    session_var='DJPERSONNEL_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def update(request, pid):
    return render(
        request, 'paf/update.html', {}
    )


@portal_auth_required(
    session_var='DJPERSONNEL_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def search(request):
    return render(
        request, 'paf/search.html', {}
    )
