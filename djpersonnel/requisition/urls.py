from django.conf.urls import url
from django.views.generic import TemplateView

from djpersonnel.requisition import views


urlpatterns = [
    # requisition create
    url(
        r'^$', views.form_home, name='requisition_form'
    ),
    url(
        r'^success/$',
        TemplateView.as_view(
            template_name='requisition/success.html'
        ),
        name='requisition_form_success'
    ),
    # requisition update
    url(
        r'^(?P<rid>\d+)/update/$',
        views.form_home, name='requisition_update'
    ),
    # requisition detail
    url(
        r'^(?P<rid>\d+)/detail/$',
        views.detail, name='requisition_detail'
    ),
    # requisition delete
    url(
        r'^(?P<rid>\d+)/delete/$',
        views.delete, name='requisition_delete'
    ),
]
