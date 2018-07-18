from django.conf.urls import include, url

from djpersonnel.dashboard import views


urlpatterns = [
    # dashboard home listing display
    url(
        r'^$',
        views.home, name='dashboard_home'
    ),
]
