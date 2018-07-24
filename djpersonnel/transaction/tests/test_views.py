# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse

from djpersonnel.transaction.models import Operation

from djtools.utils.logging import seperator


class TransactionOperationTestCase(TestCase):

    def setUp(self):
        pass

    def test_form_returns_correct_html(self):

        response = self.client.get(reverse('transaction_form'))
        self.assertTemplateUsed(response, 'transaction/form.html')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertTrue(html.strip().endswith('</html>'))

    def test_display_returns_correct_html(self):

        response = self.client.get(reverse('transaction_display'))
        self.assertTemplateUsed(response, 'transaction/display.html')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertTrue(html.strip().endswith('</html>'))

