# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.test import TestCase

from djpersonnel.transaction.models import Operation as Transaction
from djpersonnel.requisition.models import Operation as Requisition
from djpersonnel.core.forms import DateCreatedForm

from djtools.utils.test import create_test_user


class CoreViewsTestCase(TestCase):

    def setUp(self):
        self.user = create_test_user()
        self.created_at_date = settings.TEST_CREATED_AT_DATE

    def test_home(self):

        requisitions = Requisition.objects.filter(
            created_by = self.user
        )

        self.assertGreaterEqual(requisition.count(), 1)

        transactions = Transaction.objects.filter(
            created_by = self.user
        )

        self.assertGreaterEqual(transactions.count(), 1)

    def test_requisition_search(self):

        form = DateCreatedForm()

        requisitions = Requisition.objects.filter(
            created_at__gte = self.created_at_date
        )

        self.assertGreaterEqual(requisition.count(), 1)

    def test_transaction_search(self):

        transactions = Transaction.objects.filter(
            created_at__gte = self.created_at_date
        ).all()

        self.assertGreaterEqual(transactions.count(), 1)
