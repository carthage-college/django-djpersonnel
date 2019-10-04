from django.urls import path, re_path
from django.views.generic import TemplateView

from djpersonnel.requisition import views


urlpatterns = [
    # requisition create
    path(
        '', views.form_home, name='requisition_form'
    ),
    path(
        'success/',
        TemplateView.as_view(
            template_name='requisition/success.html'
        ),
        name='requisition_form_success'
    ),
    # requisition update
    re_path(
        r'^(?P<rid>\d+)/update/$', views.form_home, name='requisition_update'
    ),
    # requisition detail
    re_path(
        r'^(?P<rid>\d+)/detail/$', views.detail, name='requisition_detail'
    ),
    # requisition delete
    re_path(
        r'^(?P<rid>\d+)/delete/$', views.delete, name='requisition_delete'
    ),
]
