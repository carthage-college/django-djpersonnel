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
        r'^(?P<mod>[-\w]+)/list/$',
        views.list, name='dashboard_list'
    ),
    # proposal status view for 'approve' or 'decline' actions
    url(
        r'^operation/status/$',
        views.operation_status, name='operation_status'
    ),
]
