from django.conf.urls import url
from django.views.generic import TemplateView

from djpersonnel.requisition import views


urlpatterns = [
    # requisition form
    url(
        r'^$', views.form_home, name='requisition_form'
    ),
]
