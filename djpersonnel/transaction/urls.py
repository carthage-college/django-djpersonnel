from django.urls import path, re_path
from django.views.generic import TemplateView

from djpersonnel.transaction import views


urlpatterns = [
    # transaction form
    path(
        '',
        views.form_home, name='transaction_form'
    ),
    path(
        'success/',
        TemplateView.as_view(
            template_name='transaction/success.html'
        ),
        name='transaction_form_success'
    ),
    #
    # dashboard URLs
    #
    # transaction detail
    re_path(
        r'^(?P<tid>\d+)/detail/$', views.detail, name='transaction_detail'
    ),
    # transaction update
    re_path(
        r'^(?P<tid>\d+)/update/$', views.update, name='transaction_update'
    ),
    # requisition delete
    re_path(
        r'^(?P<tid>\d+)/delete/$', views.delete, name='transaction_delete'
    ),
    # transaction appointment letter
    re_path(
        r'^(?P<tid>\d+)/appointment-letter/$',
        views.appointment_letter, name='transaction_appointment_letter'
    ),
    # transaction graduate assistant letter
    re_path(
        r'^(?P<tid>\d+)/graduate-assistant-letter/$',
        views.graduate_assistant_letter, name='transaction_graduate_assistant_letter'
    ),
]
