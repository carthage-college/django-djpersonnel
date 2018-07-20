from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse

from djpersonnel.requisition.models import Operation

from djtools.utils.test import create_test_user

import json


class RequisitionViewsTestCase(TestCase):

    def setUp(self):

        self.user = create_test_user()

    def test_requisition_form(self):
        print("\n")
        print("PRF requisition form")
        earl = reverse('requisition_form')
        print(earl)
        # get page
        response = self.client.get(earl, follow=True)
        self.assertEqual(response.status_code, 200)

        json_data = open(
            '{}/fixtures/requisition_operation.json'.format(settings.ROOT_DIR)
        ).read()
        data = json.loads(json_data)

        requi = self.client.post(earl, data[0]['fields'])
        print(requi)

        # attempt to sign in with client login method
        #login = self.client.login(
            #username=self.user.username, password=self.user.password
        #)
        #self.assertTrue(login)
        #response = self.client.get(earl)
        #self.assertEqual(response.status_code, 200)

