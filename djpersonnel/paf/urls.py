from django.conf.urls import url
from django.views.generic import TemplateView

from djpersonnel.paf import views

urlpatterns = [
    # paf form
    url(
        r'^$',
        views.paf_form, name='paf_form'
    ),
    url(
        r'^success/$',
        TemplateView.as_view(
            template_name='paf/success.html'
        ),
        name='paf_success'
    ),
]
