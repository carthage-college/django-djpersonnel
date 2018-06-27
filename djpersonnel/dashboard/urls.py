from django.conf.urls import include, url

from djskeletor.dashboard import views


urlpatterns = [
    # dashboard home listing display
    url(
        r'^$',
        views.home, name='home'
    ),
]
