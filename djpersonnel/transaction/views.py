from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, get_object_or_404

from djpersonnel.transaction.models import Operation
from djpersonnel.transaction.forms import OperationForm

from djzbar.decorators.auth import portal_auth_required
from djzbar.utils.hr import get_position
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
            template = 'transaction/email/created_by.html'
            if not settings.DEBUG:

                # email distribution list and bcc parameters
                bcc = [settings.ADMINS[0][1],]
                # send confirmation email to user who submitted the form
                to_list = [data.created_by.email,]
                # subject
                subject = "[PAF Submission] {}, {}".format(
                    data.created_by.last_name, data.created_by.first_name
                )

                send_mail(
                    request, to_list, subject, settings.PAF_EMAIL_LIST[0],
                    template, data, bcc
                )

                # send approver email to VP or Provost
                template = 'transaction/email/approver.html'
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
                    reverse_lazy('transaction_form_success')
                )
            else:
                # display the email template
                return render(
                    request, template, {'data': data,'form':form}
                )
    else:
        form = OperationForm(label_suffix='')

    return render(
        request, 'transaction/form_bootstrap.html', {'form': form,}
    )

    # if settings.DEBUG:
    #     TO_LIST = [settings.SERVER_EMAIL,]
    # else:
    #     TO_LIST = [settings.PAF_EMAIL_LIST,]
    # BCC = settings.MANAGERS

    # if request.method=='POST':
    #     form = OperationForm(request.POST)
    #     if form.is_valid():
    #         data = form.save()
    #         email = data.created_by.email
    #         subject = "[PAF Submission] {}, {}".format(
    #             data.created_by.last_name, data.created_by.first_name
    #         )
    #         send_mail(
    #             request, TO_LIST, subject, email,'transaction/email.html',
    #             data, BCC
    #         )
    #         return HttpResponseRedirect(
    #             reverse_lazy('transaction_form_success')
    #         )
    # else:
    #     form = OperationForm()
    #
    # return render(
    #     request, 'transaction/form_bootstrap.html', {'form': form,}
    # )


@portal_auth_required(
    session_var='DJPERSONNEL_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def display(request, tid):
    data = get_object_or_404(Operation, id=tid)
    return render(
        request, 'transaction/display.html', {'data':data}
    )
# def display(request, tid):
#     data = get_object_or_404(Operation, id=tid)
#     return render(
#         request, 'transaction/display.html', {'data':data}
#     )


@portal_auth_required(
    session_var='DJPERSONNEL_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def update(request, pid):
    return render(
        request, 'transaction/update.html', {}
    )
