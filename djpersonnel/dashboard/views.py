# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy

from djpersonnel.transaction.models import Operation
from djpersonnel.dashboard.forms import DateCreatedForm

from djzbar.decorators.auth import portal_auth_required


#@portal_auth_required(
#    group='LIS', session_var='DJVISION_AUTH',
#    redirect_url=reverse_lazy('access_denied')
#)
def home(request):
    error = None
    objects = None
    if request.method == 'POST':
        form = DateCreatedForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            objects = Operation.objects.filter(
                created_at >= data['created_at']
            ).all()
    else:
        form = DateCreatedForm()

    return render(
        request, 'dashboard/home.html', {
            'form':form, 'objects':objects, 'error':error
        }
    )
