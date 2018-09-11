from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse

from djpersonnel.requisition.models import Operation

from djzbar.utils.hr import get_position
from djtools.utils.test import create_test_user

import json


class RequisitionViewsTestCase(TestCase):

    def setUp(self):

        self.user = create_test_user()
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

        json_data = open(
            '{}/fixtures/requisition_operation.json'.format(settings.ROOT_DIR)
        ).read()
        data = json.loads(json_data)
        data = data[0]['fields']
        data['level1_date'] = ''
        data['level2_date'] = ''
        data['level3_date'] = ''
        requi = self.client.post(earl, data)

        requisitions = Operation.objects.get(created_by = self.user)
        self.assertGreaterEqual(requisitions.count(), 1)

    def test_email_logic(self):

        provost = get_position(settings.LEVEL3_TPOS)
        print(provost)

