from django.conf.urls import url
from django.views.generic import TemplateView

from djpersonnel.transaction import views


urlpatterns = [
    # transaction form
    url(
        r'^$',
        views.form_home, name='transaction_form'
    ),
    url(
        r'^success/$',
        TemplateView.as_view(
            template_name='transaction/success.html'
        ),
        name='transaction_success'
    ),
    # transaction detail
    url(
        r'^(?P<aid>\d+)/display/$',
        views.display, name='transaction_display'
    ),
    # transaction update
    url(
        r'^(?P<aid>\d+)/update/$',
        views.update, name='transaction_update'
    ),
    # transaction search for operations
    url(
        r'^search/$',
        views.search, name='transaction_search'
    ),
    # listing display
    url(
        r'list/^$',
        views.list, name='transaction_list'
    ),
]
