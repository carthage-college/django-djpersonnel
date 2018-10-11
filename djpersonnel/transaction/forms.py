# -*- coding: utf-8 -*-
from django import forms

from djpersonnel.transaction.models import Operation
from djpersonnel.core.utils import level3_choices

REQUIRED_FIELDS = {
    'newhire_rehire': [
        'position_title',
        'hire_type',
        'pay_type',
        'expected_start_date',
        'budget_account',
        'position_grant_funded',
        'moving_expenses'
    ],
    'department_change': [
        'new_department', 'old_department'
    ],
    'compensation_change': [
        'current_compensation', 'new_compensation', 'salary_change_reason',
        'compensation_effective_date', 'temporary_interim_pay'
    ],
    'onetime_payment': [
        'amount', 'amount_reason', 'pay_after_date',
        'department_account_number', 'grant_pay'
    ],
    'supervisor_change': [
        'new_supervisor', 'old_supervisor'
    ],
    'termination': [
        'termination_type', 'last_day_date', 'returned_property',
        'eligible_rehire', 'vacation_days_accrued'
    ],
    'status_change': [
        'status_type', 'status_change_effective_date', 'hours_per_week'
    ],
    'position_change': [
        'old_position', 'new_position', 'position_effective_date',
        'additional_supervisor_role'
    ],
    'leave_of_absence': [
        'leave_of_absence_date', 'expected_return_date',
        'leave_of_absence_reason'
    ],
    'sabbatical': [
        'sabbatical_types', 'academic_year'
    ]
}

REQUIRED_FIELDS_NEWHIRE = {
    'staff': [
        'status_type',
        'status_change_effective_date',
        'hours_per_week',
        'offered_compensation',
        'supervise_others',
        'standard_vacation_package',
    ],
    'faculty': [
        'startup_expenses',
        'teaching_appointment',
        'employment_type',
        'program_types'
    ]
}
REQUIRED_FIELDS_ADJUNCT = ['courses_teaching','number_of_credits','music']



class OperationForm(forms.ModelForm):

    approver = forms.ChoiceField(
        label="Who will approve this request for you?",
        choices=level3_choices()
    )

    class Meta:
        model = Operation
        exclude = [
            'created_by','updated_by','created_at','updated_at',
            'level1,level1_date','level2,level2_date','level3,level3_date',
            'level3_approver','declined','email_approved'
        ]

    def dependent(self, field1, value, field2):
        cd = self.cleaned_data

        if cd.get(field1) == value and not cd.get(field2):
            self.add_error(field2, "Required field")

    def clean(self):
        cd = self.cleaned_data

        # all required fields
        for required, fields in REQUIRED_FIELDS.items():
            if cd.get(required):
                for field in fields:
                    if not cd.get(field):
                        self.add_error(field, "Required field")

        # newhire/rehire
        if cd.get('newhire_rehire'):

            # required fields for all newhire/rehire
            employee = cd.get('employee_type').lower()
            if employee:
                for field in REQUIRED_FIELDS_NEWHIRE[employee]:
                    if not cd.get(field):
                        self.add_error(field, "Required field")

            # newhire
            # moving expenses
            field = 'moving_expenses_amount'
            if cd.get('moving_expenses') == 'Yes' and not cd.get(field):
                self.add_error(field, "Required field")

            # grant funded
            if cd.get('position_grant_funded') == 'Yes':
                fields = ['grant_fund_number', 'grant_fund_amount']
                for field in fields:
                    if not cd.get(field):
                        self.add_error(field, "Required field")

            # newhire faculty
            if employee == 'faculty':
                # newhire contract
                field = 'contract_years'
                et = cd.get('employment_type')
                if et and 'Contract' in et:
                    if not cd.get(field):
                        self.add_error(field, "Required field")
                # newhire adunct
                elif et == 'Adjunct':
                    for field in REQUIRED_FIELDS_ADJUNCT:
                        if not cd.get(field):
                            self.add_error(field, "Required field")
                # teaching appointment
                self.dependent(
                    'teaching_appointment','Other','teaching_appointment_arrangements'
                )
                # startup expenses
                self.dependent('startup_expenses','Yes','startup_expenses_amount')

            # newhire staff
            if employee == 'staff':
                # vacation
                self.dependent('standard_vacation_package','No','vacation_days')
                # shift if department_name = EVS
                self.dependent('department_name','EVS','shift')

        # various dependent fields
        if cd.get('compensation_change'):
            self.dependent('temporary_interim_pay', 'Yes', 'end_date')
        if cd.get('position_change'):
            self.dependent('additional_supervisor_role', 'Yes', 'direct_reports')
        if cd.get('onetime_payment'):
            self.dependent('grant_pay', 'Yes', 'grant_pay_account_number')
        if cd.get('termination'):
            tt = cd.get('termination_type')
            if (tt == 'Voluntary' or tt == 'Involuntary') and \
              (not cd.get('termination_voluntary') or cd.get('termination_voluntary') == ''):
                self.add_error(
                    'termination_{}'.format(tt.lower()), "Please select a reason"
                )

        return cd
