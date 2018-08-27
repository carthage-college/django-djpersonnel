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
    #
    # dashboard URLs
    #
    # transaction detail
    url(
        r'^(?P<tid>\d+)/display/$',
        views.display, name='transaction_display'
    ),
    # transaction update
    url(
        r'^(?P<aid>\d+)/update/$',
        views.update, name='transaction_update'
    ),
    # transaction appointment letter
    url(
        r'^(?P<tid>\d+)/appointment_letter/$',
        views.appointment_letter, name='transaction_appointment_letter'
    ),
]
