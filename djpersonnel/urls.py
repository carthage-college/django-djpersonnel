# -*- coding: utf-8 -*-

from django.urls import include
from django.urls import path
from django.urls import reverse_lazy
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.contrib import admin
from djpersonnel.core.views import home
from djauth.views import loggedout


admin.autodiscover()

handler404 = 'djtools.views.errors.four_oh_four_error'
handler500 = 'djtools.views.errors.server_error'


urlpatterns = [
    # auth
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(),
        {'template_name': 'registration/login.html'},
        name='auth_login',
    ),
    path(
        'accounts/logout/',
        auth_views.LogoutView.as_view(),
        {'next_page': reverse_lazy('auth_loggedout')},
        name='auth_logout',
    ),
    path(
        'accounts/loggedout/',
        loggedout,
        {'template_name': 'registration/logged_out.html'},
        name='auth_loggedout',
    ),
    path(
        'accounts/',
        RedirectView.as_view(url=reverse_lazy('auth_login')),
    ),
    path(
        'denied/',
        TemplateView.as_view(template_name='denied.html'),
        name='access_denied',
    ),
    # django admin
    path('rocinante/', include('loginas.urls')),
    path('rocinante/', admin.site.urls),
    # admin honeypot
    #path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    # dashboard
    path('dashboard/', include('djpersonnel.core.urls')),
    # finance URLs
    path('finance/', include('djpersonnel.finance.urls')),
    # personnel requisition form
    path('requisition/', include('djpersonnel.requisition.urls')),
    # personnel transaction form
    path('transaction/', include('djpersonnel.transaction.urls')),
    # redirect home to dashboard
    path('', home, name='dashboard_home'),
]
