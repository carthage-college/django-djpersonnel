# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import resolve
from django.conf import settings
from django.test import TestCase
from django.http import HttpRequest
from django.core.urlresolvers import reverse

from djpersonnel.transaction.views import form_home

from djtools.utils.logging import seperator
from djzbar.utils.informix import get_session
from djzbar.settings import INFORMIX_EARL_TEST as EARL


class TransactionOperationTestCase(TestCase):

    def setUp(self):
        pass

    def test_form_returns_correct_html(self):
        print("\n")
        print("test form view")
        seperator()
        #request = HttpRequest()
        #response = form_home(request)
        response = self.client.get(reverse('transaction_form'))
        self.assertTemplateUsed(response, 'transaction/form.html')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertTrue(html.strip().endswith('</html>'))


