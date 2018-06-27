from django.conf import settings
from django.shortcuts import render



def home(request):
    return render(
        request, 'dashboard/paf/home.html', {}
    )


def paf_display(request, pid):
    return render(
        request, 'dashboard/paf/display.html', {}
    )


def paf_update(request, pid):
    return render(
        request, 'dashboard/paf/update.html', {}
    )


def paf_search(request):
    return render(
        request, 'dashboard/paf/search.html', {}
    )
