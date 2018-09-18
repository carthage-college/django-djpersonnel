# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from unittest import skip

from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import User

from djpersonnel.requisition.models import Operation

from djtools.utils.test import create_test_user

from datetime import datetime


#@skip('skip class')
class RequisitionModelsTestCase(TestCase):

    fixtures = [
        'fixtures/user.json','fixtures/requisition_operation.json'
    ]

    def setUp(self):
        self.year = 2020
        self.month = 5
        self.day = 1
        self.user = create_test_user()
        self.date = datetime(self.year, self.month, self.day)
        self.level3_approver = User.objects.get(
            pk=settings.TEST_LEVEL3_APPROVER_ID
        )

    def test_operation(self):

        # create
        obj = Operation.objects.create(
            created_by = self.user, updated_by = self.user, new_position='No',
            expected_start_date = self.date, salary_type = 'Non-exempt',
            position_title = 'Slacker', department_name = 'MAIN',
            account_number = '90120', budgeted_position = 'Yes',
            min_salary_range = 39000.00, mid_salary_range = 49000.00,
            max_salary_range = 69000.00, position_open_date = self.date,
            publication_date = self.date, hours_per_week = '37.5',
            level3_approver = self.level3_approver,
            replacement_name = 'Kir Kroker', applicant_system = 'Yes',
            applicant_system_people = 'larry kurkowski',
            job_description = "", speciality_sites = 'Yes',
            speciality_sites_urls = 'https://www.stackexchange.com/',
        )

        obj.save()

        objects = Operation.objects.all()
        self.assertEqual(Operation.objects.count(), 3)

        op = Operation.objects.filter(created_by=self.user)
        self.assertEqual(op.count(), 3)

        # update
        obj.title = 'test update operation object'
        obj.save_submit = True
        obj.save()

        # delete
        Operation.objects.filter(expected_start_date__year=self.year).delete()
