from django.conf.urls import url
from django.views.generic import TemplateView

from djpersonnel.requisition import views


urlpatterns = [
    # requisition form
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
    #
    # dashboard URLs
    #
    # transaction detail
    url(
        r'^(?P<rid>\d+)/detail/$',
        views.detail, name='requisition_detail'
    ),
    # transaction update
    url(
        r'^(?P<aid>\d+)/update/$',
        views.update, name='requisition_update'
    ),
]
