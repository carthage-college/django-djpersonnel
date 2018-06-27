from django.conf import settings
from django.shortcuts import render


def home(request):
    return render(
        request, 'dashboard/home.html', {}
    )


def search(request):
    return render(
        request, 'dashboard/search.html', {}
    )

