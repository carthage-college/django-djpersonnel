# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from unittest import skip, skipIf, skipUnless

from django.conf import settings
from django.test import TestCase
from django.core import serializers
from django.contrib.auth.models import User

from djpersonnel.transaction.models import Operation

from djtools.utils.test import create_test_user

from djtools.utils.logging import seperator

from datetime import datetime

import json


#@skip('skip class')
class TransactionModelsTestCase(TestCase):

    fixtures = [
        'fixtures/group.json', 'fixtures/user.json',
    ]

    def setUp(self):

        global tid, json_data
        data = 7

        self.year = 2020
        self.month = 5
        self.day = 1
        self.user = create_test_user()
        self.expected_start_date = datetime(self.year, self.month, self.day)
        # sample object
        json_data = open(
            '{}/fixtures/transaction_operation.json'.format(settings.ROOT_DIR)
        ).read()

    #@skip('skip to my loo')
    def test_operation(self):

        # create object from json fixture data

        obj_generator = serializers.json.Deserializer(json_data)
        for obj in obj_generator:
            obj.save()

        objects = Operation.objects.all()
        self.assertEqual(Operation.objects.count(), 1)

        op = Operation.objects.get(created_by=self.user)
        # obj is a deserialized object with 'object' as an attribute
        # that contains the Operation() data
        self.assertTrue(op.id == obj.object.id)

        # update
        obj.position_title = 'test update operation object'
        obj.level1 = True
        obj.save()

        # delete
        Operation.objects.filter(expected_start_date__year=self.year).delete()
