from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import User

from djtools.utils.test import create_test_user

from djpersonnel.transaction.forms import OperationForm

import json


class TransactionOperationTestCase(TestCase):

    fixtures = [
        'fixtures/user.json'
    ]

    def setUp(self):

        global data

        self.user = create_test_user()
        self.level3_approver_id = settings.TEST_LEVEL3_APPROVER_ID
        self.level3_approver = User.objects.get(
            pk=self.level3_approver_id
        )
        # sample object
        json_data = open(
            '{}/fixtures/transaction_operation.json'.format(settings.ROOT_DIR)
        ).read()
        # dictionary data
        data = json.loads(json_data)[0]['fields']

    def test_operation_form_valid_data(self):

        form = OperationForm(self.data)
        form.is_valid()
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_operation_form_invalid_data(self):
        self.data['last_name'] = ''
        form = OperationForm(self.data)
        self.assertFalse(form.is_valid())

    def test_operation_form_blank_data(self):
        form = OperationForm({})
        self.assertFalse(form.is_valid())
