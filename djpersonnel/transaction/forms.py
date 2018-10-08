# -*- coding: utf-8 -*-
from django import forms

from djpersonnel.transaction.models import Operation
from djpersonnel.core.utils import level3_choices

REQUIRED_FIELDS = {
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
        'status_type', 'status_change_effective_date'
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

    def clean(self):
        cd = self.cleaned_data

        for required, fields in REQUIRED_FIELDS.items():
            if cd.get(required):
                for field in fields:
                    if not cd.get(field):
                        self.add_error(field, "Required field")

        # dependant fields
        if cd.get('temporary_interim_pay') == 'Yes' and not cd.get('end_date'):
            self.add_error('end_date', "Please provide an end date")

        if cd.get('grant_pay') == 'Yes' and not cd.get('grant_pay_account_number'):
            self.add_error(
                'grant_pay_account_number', "Please provide an account number"
            )

        if cd.get('additional_supervisor_role') == 'Yes' and not cd.get('direct_reports'):
            self.add_error(
                'direct_reports', "Please provide the names of direct reports"
            )

        tt = cd.get('termination_type')
        if (tt == 'Voluntary' or tt == 'Involuntary') and \
          (not cd.get('termination_voluntary') or cd.get('termination_voluntary') == ''):
            self.add_error(
                'termination_{}'.format(tt.lower()), "Please select a reason"
            )

        return cd

