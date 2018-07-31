# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.test import TestCase

from djpersonnel.transaction.models import Operation as Transaction
from djpersonnel.requisition.models import Operation as Requisition
from djpersonnel.dashboard.forms import DateCreatedForm

from djtools.utils.logging import seperator


class DashboardViewsTestCase(TestCase):

    def setUp(self):
        self.created_at_date = settings.TEST_CREATED_AT_DATE

    def test_transaction_created_at(self):
        print("\n")
        print("select all PAF transactions after a specific date")
        seperator()

        form = DateCreatedForm()

        objects = Transaction.objects.filter(
            created_at__gte = self.created_at_date
        ).all()

        self.assertGreaterEqual(objects.count(), 1)
