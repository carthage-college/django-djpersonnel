from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, Http404

from djzbar.decorators.auth import portal_auth_required



def home(request):
    '''
    dashboard home page view
    '''

    return render(
        request, 'home.html', {}
    )
