# -*- coding: utf-8 -*-

from django.urls import include
from django.urls import path


urlpatterns = [
    # Budget URLs
    path('budget/', include('djpersonnel.finance.budget.urls')),
]
