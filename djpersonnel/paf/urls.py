from django.conf.urls import url
from django.views.generic import TemplateView

from djpersonnel.paf import views


urlpatterns = [
    # paf form
    url(
        r'^$',
        views.form, name='paf_form'
    ),
    url(
        r'^success/$',
        TemplateView.as_view(
            template_name='paf/success.html'
        ),
        name='paf_success'
    ),
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
        r'list/^$',
        views.list, name='paf_list'
    ),
]
