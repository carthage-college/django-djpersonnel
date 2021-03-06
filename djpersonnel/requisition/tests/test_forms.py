from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import User

from djpersonnel.requisition.forms import OperationForm


class RequistionOperationTestCase(TestCase):

    fixtures = [
        'fixtures/user.json','fixtures/requisition_operation.json'
    ]

    def setUp(self):

        self.user = User.objects.get(pk=settings.TEST_USER_ID)
        self.level3_approver_id = settings.TEST_LEVEL3_APPROVER_ID
        self.level3_approver = User.objects.get(pk=self.level3_approver_id)
        self.data = {
            'position_title': 'Bender','department_name': 'MAIN',
            'account_number': '8675309', 'new_position': 'No',
            'replacement_name': 'Kir Kroker', 'budgeted_position': 'Yes',
            'account_number': '8675309', 'salary_type': 'Non-exempt',
            'hours_per_week': '37.5', 'min_salary_range': '39000.00',
            'mid_salary_range': '49000.00','max_salary_range': '69000.00',
            'position_open_date':'2018-04-20','publication_date':'2018-02-02',
            'expected_start_date': '2018-05-01', 'applicant_system': 'Yes',
            'applicant_system_people': 'Larry', 'speciality_sites': 'Yes',
            'speciality_sites_urls': 'https://serverfault.com/',
            'created_by': self.user.id,'level3_approver': self.level3_approver,
            'approver': self.level3_approver_id
        }

    def test_operation_form_valid_data(self):

        form = OperationForm(self.data)
        self.assertTrue(form.is_valid())

    def test_operation_form_invalid_data(self):
        data = self.data
        data['speciality_sites_urls'] = ''
        form = OperationForm(data)
        self.assertFalse(form.is_valid())

    def test_operation_form_blank_data(self):
        form = OperationForm({})
        self.assertFalse(form.is_valid())
