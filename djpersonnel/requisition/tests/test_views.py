# -*- coding: utf-8 -*-
from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from djpersonnel.requisition.models import Operation

from unittest import skip, skipIf, skipUnless

import json


class RequisitionViewsTestCase(TestCase):

    fixtures = [
        'fixtures/group.json', 'fixtures/user.json',
        'fixtures/requisition_operation.json'
    ]

    def setUp(self):

        self.oid = 7
        self.user = User.objects.get(pk=settings.TEST_USER_ID)
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

    def test_requisition_form(self):
        earl = reverse('requisition_form')
        # get page
        response = self.client.get(earl, follow=True)
        self.assertEqual(response.status_code, 200)

        # attempt to sign in with client login method
        login = self.client.login(
            username=self.user.username, password=self.password
        )
        self.assertTrue(login)
        response = self.client.get(earl)
        self.assertEqual(response.status_code, 200)
        # obtain data from json fixture
        json_data = open(
            '{}/fixtures/requisition_operation.json'.format(settings.ROOT_DIR)
        ).read()
        data = json.loads(json_data)
        data = data[0]['fields']
        data['level1_date'] = ''
        data['level2_date'] = ''
        data['level3_date'] = ''
        data['level3_approver'] = settings.TEST_LEVEL3_APPROVER_ID
        requi = self.client.post(earl, data)
        requisitions = Operation.objects.filter(created_by = self.user)
        self.assertGreaterEqual(requisitions.count(), 1)

    def test_requisition_detail(self):

        data = get_object_or_404(Operation, id=self.oid)
        # creator
        user = self.user
        perms = data.permissions(user)
        self.assertTrue(perms['view'])
        # level3
        user = self.level3_approver
        perms = data.permissions(user)
        self.assertTrue(perms['view'])
        self.assertTrue(perms['level3'])
        self.assertTrue(perms['approver'])
        # level2
        user = self.level2_approver
        perms = data.permissions(user)
        self.assertTrue(perms['view'])
        self.assertTrue(perms['level2'])
        self.assertTrue(perms['approver'])
        # level1
        user = self.level1_approver
        perms = data.permissions(user)
        self.assertTrue(perms['view'])
        self.assertTrue(perms['level1'])
        self.assertTrue(perms['approver'])

    def test_requisition_delete(self):

        # attempt to sign in with client login method
        login = self.client.login(
            username=self.level1_approver.username, password=self.password
        )
        self.assertTrue(login)
        # get delete URL
        earl = reverse('requisition_delete', kwargs={'rid': self.oid})
        response = self.client.get(earl)
        # response should be redirect to dashboard home
        self.assertEqual(response.status_code, 302)
