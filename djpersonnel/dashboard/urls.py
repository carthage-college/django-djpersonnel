from django.conf.urls import url

from djskeletor.dashboard import views

urlpatterns = [
    # paf detail
    url(
        r'^paf/(?P<pid>\d+)/display/$',
        views.display, name='paf_operation_display'
    ),
    # paf update
    url(
        r'^paf/(?P<pid>\d+)/update/$',
        views.display, name='paf_update'
    ),
    # paf search for operations
    url(
        r'^paf/search/$',
        views.paf_search, name='paf_search'
    ),
    # home listing display
    url(
        r'^$',
        views.home, name='home'
    ),
]
