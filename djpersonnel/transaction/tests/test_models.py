# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from unittest import skip, skipIf, skipUnless

from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import User

from djpersonnel.transaction.models import Operation

from djtools.utils.test import create_test_user

from djtools.utils.logging import seperator

from datetime import datetime


#@skip('skip class')
class TransactionModelsTestCase(TestCase):

    def setUp(self):
        self.year = 2020
        self.month = 5
        self.day = 1
        self.user = create_test_user()
        self.start_date = datetime(self.year, self.month, self.day)

    @skip('skip to my loo')
    def test_operation(self):

        # create
        obj = Operation.objects.create(
            created_by = self.user, updated_by = self.user,
            start_date = self.start_date,
            title = 'test operation', comments = 'hello world'
        )
        obj.save()

        objects = Operation.objects.all()
        self.assertEqual(Operation.objects.count(), 1)

        op = Operation.objects.get(created_by=self.user)
        self.assertTrue(op.id == obj.id)

        # update
        obj.title = 'test update operation object'
        obj.save_submit = True
        obj.save()

        # delete
        Operation.objects.filter(start_date__year=self.year).delete()
