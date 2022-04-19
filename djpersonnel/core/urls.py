# -*- coding: utf-8 -*-

from django.urls import include
from django.urls import path
from djpersonnel.core import views


urlpatterns = [
    # complete lising
    path('<str:mod>/list/', views.list, name='dashboard_list'),
    # export to openxml
    path('<str:mod>/openxml/', views.openxml, name='openxml'),
    # approver manager
    path('approver/', views.approver_manager, name='approver_manager'),
    # proposal status view for 'approve' or 'decline' actions
    path('operation/status/', views.operation_status, name='operation_status'),
    # dashboard home listing display
    path('', views.home, name='dashboard_home'),
]
