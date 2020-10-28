from django.urls import include, path, re_path

from djpersonnel.core import views


urlpatterns = [
    # complete lising
    re_path(
        r'^(?P<mod>[-\w]+)/list/$', views.list, name='dashboard_list',
    ),
    # export to openxml
    re_path(
        r'^(?P<mod>[-\w]+)/openxml/$', views.openxml, name='openxml',
    ),
    # approver manager
    path(
        'approver/', views.approver_manager, name='approver_manager',
    ),
    # proposal status view for 'approve' or 'decline' actions
    path(
        'operation/status/', views.operation_status, name='operation_status',
    ),
    # dashboard home listing display
    path('', views.home, name='dashboard_home'),
]
urlpatterns += path('admin/', include('loginas.urls')),
