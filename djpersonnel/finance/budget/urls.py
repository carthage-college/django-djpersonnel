# -*- coding: utf-8 -*-

from django.urls import path
from django.views.generic import TemplateView
from djpersonnel.finance.budget import views


urlpatterns = [
    # create success
    path(
        'success/',
        TemplateView.as_view(template_name='finance/budget/success.html'),
        name='budget_form_success',
    ),
    # budget update
    path('<int:bid>/update/', views.home, name='budget_update'
    ),
    # budget detail
    path('<int:bid>/detail/', views.detail, name='budget_detail'),
    # budget delete
    path('<int:bid>/delete/', views.delete, name='budget_delete'),
    # budget create
    path('', views.home, name='budget_form'),
]
