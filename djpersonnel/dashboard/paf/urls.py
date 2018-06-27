from django.conf.urls import url

from djskeletor.dashboard.paf import views


urlpatterns = [

    # paf detail
    url(
        r'^(?P<pid>\d+)/display/$',
        views.display, name='paf_display'
    ),
    # paf update
    url(
        r'^(?P<pid>\d+)/update/$',
        views.update, name='paf_update'
    ),
    # paf search for operations
    url(
        r'^search/$',
        views.search, name='paf_search'
    ),
    # listing display
    url(
        r'^$',
        views.home, name='home'
    ),
]
