from django.conf import settings
from django.test import TestCase

from djtools.utils.test import create_test_user

from djpersonnel.requisition.forms import OperationForm


class OperationTestCase(TestCase):

    fixtures = [
        'fixtures/user.json','fixtures/requisition_operation.json'
    ]

    def setUp(self):
        self.user = create_test_user()
        self.data = {
            'position_title': 'Bender','department_name': 'Delivery',
            'account_number': '8675309','replacement_for': True,
            'replacement_name': 'Kir Kroker','new_position': True,
            'budgeted_position': True,'min_salary_range': '39000.00',
            'mid_salary_range': '49000.00','max_salary_range': '69000.00',
            'position_open_date': '2018-04-20',
            'expected_start_date': '2018-05-01','hours_per_week': '37.5',
            'weekly_schedule': 'MTWRF','hiring_mgr_name': 'turanga leela',
            'hiring_mgr_date': '2018-04-20','vp_provost_name': 'Amy Wong',
            'vp_provost_date': '2018-05-01','cfo_name': 'Hubert J. Farnsworth',
            'cfo_date': '2018-05-01','hr_name': 'Hermes Conrad',
            'hr_date': '2018-05-01','comments': 'nice.',
            'created_by': self.user.id
        }

    def test_operation_form_valid_data(self):

        form = OperationForm(self.data)
        self.assertTrue(form.is_valid())

    def test_operation_form_invalid_data(self):
        data = self.data
        data['created_by'] = 8675309
        form = OperationForm(data)
        self.assertFalse(form.is_valid())

    def test_operation_form_blank_data(self):
        form = OperationForm({})
        self.assertFalse(form.is_valid())
        #print(form.errors)
