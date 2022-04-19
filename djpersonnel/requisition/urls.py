# -*- coding: utf-8 -*-

from django.urls import path
from django.views.generic import TemplateView
from djpersonnel.requisition import views


urlpatterns = [
    # create success
    path(
        'success/',
        TemplateView.as_view(template_name='requisition/success.html'),
        name='requisition_form_success',
    ),
    # requisition update
    path('<int:rid>/update/', views.form_home, name='requisition_update'
    ),
    # requisition detail
    path('<int:rid>/detail/', views.detail, name='requisition_detail'),
    # requisition delete
    path('<int:rid>/delete/', views.delete, name='requisition_delete'),
    # requisition create
    path('', views.form_home, name='requisition_form'),
]
