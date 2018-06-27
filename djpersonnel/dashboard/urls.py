from django.conf.urls import include, url

from djskeletor.dashboard import views


urlpatterns = [
    # personnel action form
    url(
        r'^paf/', include('djpersonnel.dashboard.paf.urls')
    ),
    # dashboard home listing display
    url(
        r'^$',
        views.home, name='home'
    ),
]
