# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from djpersonnel.transaction.models import Operation

from djtools.utils.logging import seperator
from djtools.utils.test import create_test_user

from unittest import skip, skipIf, skipUnless


class TransactionOperationTestCase(TestCase):

    fixtures = [
        'fixtures/group.json', 'fixtures/user.json',
        'fixtures/transaction_operation.json'
    ]

    def setUp(self):

        global tid
        tid = 7

        self.user = create_test_user()
        self.level3_approver = User.objects.get(
            pk=settings.TEST_LEVEL3_APPROVER_ID
        )
        self.level2_approver = User.objects.get(
            pk=settings.TEST_LEVEL2_APPROVER_ID
        )
        self.level1_approver = User.objects.get(
            pk=settings.TEST_LEVEL1_APPROVER_ID
        )
        self.password = settings.TEST_USER_PASSWORD

        # attempt to sign in with client login method
        login = self.client.login(
            username=self.level1_approver.username, password=self.password
        )
        self.assertTrue(login)

    def test_form_returns_correct_html(self):

        response = self.client.get(reverse('transaction_form'))
        self.assertTemplateUsed(response, 'transaction/form_bootstrap.html')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertTrue(html.strip().endswith('</html>'))

    def test_detail_returns_correct_html(self):

        # get detail url
        response = self.client.get(
            reverse('transaction_detail', kwargs={'tid': tid})
        )
        self.assertTemplateUsed(response, 'transaction/detail.html')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertTrue(html.strip().endswith('</html>'))

    def test_transaction_delete(self):

        # get delete URL
        earl = reverse('transaction_delete', kwargs={'tid': tid})
        response = self.client.get(earl)
        # response should be redirect to dashboard home
        self.assertEqual(response.status_code, 302)
        # was it deleted?
        try:
            obj = Operation.objects.get(pk=tid)
        except:
            obj = None
        self.assertEqual(obj, None)
