from django.urls import path, re_path
from django.views.generic import TemplateView

from djpersonnel.transaction import views


urlpatterns = [
    # transaction form
    path('', views.form_home, name='transaction_form'),
    path(
        'success/',
        TemplateView.as_view(template_name='transaction/success.html'),
        name='transaction_form_success',
    ),
    #
    # dashboard URLs
    #
    # transaction detail
    path('<int:tid>/detail/', views.detail, name='transaction_detail'),
    # transaction update
    path('<int:tid>/update/', views.update, name='transaction_update'),
    # requisition delete
    path('<int:tid>/delete/', views.delete, name='transaction_delete'),
    # transaction appointment letter
    path(
        '<int:tid>/appointment-letter/',
        views.appointment_letter,
        name='transaction_appointment_letter',
    ),
    # transaction graduate assistant letter
    path(
        '<int:tid>/graduate-assistant-letter/',
        views.graduate_assistant_letter,
        name='transaction_graduate_assistant_letter',
    ),
    # print select transactions
    path('print/', views.paf_print, name='paf_print'),
]
