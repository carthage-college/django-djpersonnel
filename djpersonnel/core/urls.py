from django.conf.urls import include, url

from djpersonnel.core import views


urlpatterns = [
    # dashboard home listing display
    url(
        r'^$',
        views.home, name='dashboard_home'
    ),
    # complete lising
    url(
        r'^(?P<mod>[-\w]+)/list/$', views.list, name='dashboard_list'
    ),

    # export to openxml
    url(
        r'^(?P<mod>[-\w]+)/openxml/$', views.openxml, name='openxml'
    ),
    # approver manager
    url(
        r'^approver/$',
        views.approver_manager, name='approver_manager'
    ),
    # proposal status view for 'approve' or 'decline' actions
    url(
        r'^operation/status/$',
        views.operation_status, name='operation_status'
    ),
]
