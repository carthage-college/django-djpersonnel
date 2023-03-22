# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse_lazy
from djauth.decorators import portal_auth_required
from djpersonnel.core.utils import get_level2
from djpersonnel.finance.budget.forms import BudgetForm
from djpersonnel.finance.budget.models import Operation as Budget
from djtools.utils.mail import send_mail
from djtools.utils.users import in_group


@portal_auth_required(
    session_var='DJPERSONNEL_AUTH',
    redirect_url=reverse_lazy('access_denied'),
)
def dashboard(request):
    """Budget workflow dashboard view."""
    user = request.user
    hr = in_group(user, settings.HR_GROUP)
    # HR or VPFA can access all objects
    if hr or user.id == get_level2().id:
        budgets = Budget.objects.all().order_by('-created_at')[:100]
    else:
        budgets = Budget.objects.filter(
            Q(created_by=user) | Q(cost_center__user=user)
        ).order_by('-created_at')[:100]

    return render(
        request,
        'finance/budget/dashboard.html',
        {'hr': hr, 'budgets': budgets},
    )


@portal_auth_required(
    session_var='DJPERSONNEL_AUTH',
    redirect_url=reverse_lazy('access_denied'),
)
def home(request, bid=None):
    """Budget workflow form."""
    user = request.user
    obj = None
    if bid:
        obj = get_object_or_404(Budget, pk=bid)
        # only HR folks can update Budget at the moment
        if not in_group(user, settings.HR_GROUP):
            return HttpResponseRedirect(reverse_lazy('access_denied'))

    if request.method=='POST':
        form = BudgetForm(
            data=request.POST,
            instance=obj,
            files=request.FILES,
            label_suffix='',
            use_required_attribute=False,
        )
        if form.is_valid():
            data = form.save(commit=False)
            data.created_by = user
            data.updated_by = user
            data.save()
            # send email to creator and approver or display it for dev
            template = 'finance/budget/approver.html'
            to_list = settings.BUDGET_LIST
            to_list.append(data.cost_center.officer.email)
            if data.gift or data.grant:
                to_list.extend(settings.BUDGET_GRANTS_GIFTS_LIST)
            bcc = [settings.ADMINS[0][1]]
            if not settings.DEBUG:
                # send email to cost center officer and CFO
                send_mail(
                    request,
                    to_list,
                    subject,
                    data.created_by.email,
                    template,
                    data,
                    bcc,
                )
                # send confirmation email to user who submitted the form
                to_list = [data.created_by.email]
                # subject
                subject = "[Budget Submission] {0}, {1}".format(
                    data.created_by.last_name, data.created_by.first_name,
                )
                template = 'finance/budget/created_by.html'
                send_mail(
                    request,
                    to_list,
                    subject,
                    settings.HR_EMAIL,
                    template,
                    data,
                    bcc,
                )
                return HttpResponseRedirect(reverse_lazy('budget_form_success'))
            else:
                # display the approver email template
                return render(
                    request, template, {'data': data, 'form': form, 'to_list': to_list},
                )
    else:
        form = BudgetForm(
            instance=obj,
            label_suffix='',
            use_required_attribute=False,
        )

    hr = in_group(user, settings.HR_GROUP)
    return render(request, 'finance/budget/form.html', {'hr': hr, 'form': form})


@portal_auth_required(
    session_var='DJPERSONNEL_AUTH',
    redirect_url=reverse_lazy('access_denied'),
)
def detail(request, bid):
    """Display the detailed data set for this budget."""
    data = get_object_or_404(Budget, pk=bid)
    user = request.user
    perms = data.permissions(user)
    if not perms['view']:
        raise Http404

    hr = in_group(user, settings.HR_GROUP)
    return render(
        request,
        'finance/budget/detail.html',
        {'hr': hr, 'data': data, 'perms': perms},
    )


@portal_auth_required(
    group = settings.HR_GROUP,
    session_var='DJPERSONNEL_AUTH',
    redirect_url=reverse_lazy('access_denied'),
)
def delete(request, bid):
    """Delete an instance of the Budget object class."""
    obj = get_object_or_404(Budget, pk=bid)
    title = obj.version
    obj.delete()
    messages.add_message(
        request,
        messages.SUCCESS,
        "Budget {0} was deleted.".format(version),
        extra_tags='alert-success',
    )
    # there is no referer in unit tests
    redirect = request.META.get('HTTP_REFERER')
    if not redirect:
        redirect = reverse_lazy('budget_dashboard')

    return HttpResponseRedirect(redirect)
