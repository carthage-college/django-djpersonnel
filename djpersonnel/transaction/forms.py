# -*- coding: utf-8 -*-
from django import forms

from djpersonnel.transaction.models import (
    ACADEMIC_YEARS, Operation, TEACHING_APPOINTMENT_CHOICES
)
from djpersonnel.core.utils import level3_choices
from djtools.utils.convert import str_to_class

REQUIRED_FIELDS = {
    'newhire_rehire': [
        'position_title',
        'hire_type',
        'pay_type',
        'expected_start_date',
        'offered_compensation',
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
        'eligible_rehire'
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
        'sabbatical_types', 'sabbatical_academic_years'
    ]
}
REQUIRED_FIELDS_NEWHIRE = {
    'staff': [
        'status_type',
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
REQUIRED_FIELDS_GRANT_FUNDED = ['grant_fund_number', 'grant_fund_amount']


class NewhireRehireForm(forms.Form):

    # required for both faculty and staff
    position_title = forms.CharField()
    hire_type = forms.TypedChoiceField()
    pay_type = forms.TypedChoiceField()
    expected_start_date = forms.DateField()
    budget_account = forms.CharField()
    offered_compensation = forms.DecimalField()
    #
    position_grant_funded = forms.TypedChoiceField()
    grant_fund_number = forms.CharField(required=False)
    grant_fund_amount = forms.CharField(required=False)
    #
    moving_expenses = forms.TypedChoiceField()
    moving_expenses_amount = forms.CharField(False)
    #
    # faculty
    #
    startup_expenses = forms.TypedChoiceField(required=False)
    startup_expenses_amount = forms.CharField(required=False)
    #
    teaching_appointment = forms.TypedChoiceField(required=False)
    teaching_appointment_arrangements = forms.CharField(required=False)
    # if employment type = Adjunct then 'music' if 'yes' courses and credits
    employment_type = forms.TypedChoiceField(required=False)
    music = forms.TypedChoiceField(required=False)
    courses_teaching = forms.CharField(required=False)
    number_of_credits = forms.CharField(required=False)
    # employment type = Contract-*
    contract_years = forms.CharField(required=False)
    # eomployment type = Graduate Assistant
    academic_term = forms.TypedChoiceField(required=False)
    expected_end_date = forms.DateField(required=False)
    food_allowance = forms.TypedChoiceField(required=False)
    first_seven_week_amount = forms.CharField(required=False)
    second_seven_week_amount = forms.CharField(required=False)
    # no dependencies
    program_types = forms.TypedChoiceField(required=False)
    #
    # staff
    #
    status_type = forms.TypedChoiceField(required=False)
    hours_per_week = forms.CharField(required=False)
    other_arrangements = forms.CharField(required=False)
    #
    supervise_others = forms.TypedChoiceField(required=False)
    #
    standard_vacation_package = forms.TypedChoiceField(required=False)
    vacation_days = forms.CharField(required=False)
    # department_name = 'EVS'
    shift = forms.TypedChoiceField(required=False)
# short cut for checkbox field name
newhire_rehire = NewhireRehireForm


class DepartmentChangeForm(forms.Form):
    new_department = forms.TypedChoiceField()
    old_department = forms.TypedChoiceField()
# short cut for checkbox field name
department_change = DepartmentChangeForm


class CompensationChangeForm(forms.Form):
    current_compensation = forms.CharField()
    new_compensation = forms.CharField()
    salary_change_reason = forms.CharField()
    compensation_effective_date = forms.DateField()
    temporary_interim_pay = forms.TypedChoiceField()
    end_date = forms.DateField(required=False)
# short cut for checkbox field name
compensation_change = CompensationChangeForm


class OnetimePaymentForm(forms.Form):
    amount = forms.DecimalField()
    amount_reason = forms.CharField()
    pay_after_date = forms.DateField()
    department_account_number = forms.CharField()
    grant_pay = forms.TypedChoiceField()
    grant_pay_account_number = forms.CharField(required=False)
# short cut for checkbox field name
onetime_payment = OnetimePaymentForm


class SupervisorChangeForm(forms.Form):
    new_supervisor = forms.CharField()
    old_supervisor = forms.CharField()
# short cut for checkbox field name
supervisor_change = SupervisorChangeForm


class TerminationForm(forms.Form):
    termination_type = forms.TypedChoiceField()
    last_day_datea = forms.DateField()
    returned_property = forms.CharField()
    eligible_rehire = forms.TypedChoiceField()
    vacation_days_accrued = forms.CharField(required=False)
    termination_voluntary = forms.TypedChoiceField(required=False)
    termination_involuntary = forms.TypedChoiceField(required=False)
# short cut for checkbox field name
termination = TerminationForm


class StatusChangeForm(forms.Form):
    status_type = forms.TypedChoiceField()
    status_change_effective_date = forms.DateField()
    hours_per_week = forms.CharField()
# short cut for checkbox field name
status_change = StatusChangeForm


class PositionChangeForm(forms.Form):
    old_position = forms.CharField()
    new_position = forms.CharField()
    position_effective_date = forms.DateField()
    additional_supervisor_role = forms.TypedChoiceField()
    direct_reports = forms.CharField(required=False)
# short cut for checkbox field name
position_change = PositionChangeForm


class LeaveOfAbsenceForm(forms.Form):
    leave_of_absence_date = forms.DateField()
    expected_return_date = forms.DateField()
    leave_of_absence_reason = forms.CharField()
# short cut for checkbox field name
leave_of_absence = LeaveOfAbsenceForm


class SabbaticalForm(forms.Form):
    sabbatical_types = forms.TypedChoiceField()
    sabbatical_academic_years = forms.CharField()
# short cut for checkbox field name
sabbatical = SabbaticalForm


class OperationForm(forms.ModelForm):

    teaching_appointment = forms.ChoiceField(
        label = "Teaching appointment",
        widget=forms.RadioSelect,
        choices=TEACHING_APPOINTMENT_CHOICES,
        required = False
    )
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
        elif cd.get(field1) != value:
            cd[field2] = None

    def clean(self):
        cd = self.cleaned_data

        # needed everywhere
        employee = cd.get('employee_type').lower()
        # all required fields
        for required, fields in REQUIRED_FIELDS.items():
            if cd.get(required):
                for field in fields:
                    if not cd.get(field):
                        self.add_error(field, "Required field")
            else:
                # set fields to null
                if cd.get('newhire_rehire') and required == 'status_change':
                    # we only need effective date for 'status_change'
                    edate = cd.get('status_change_effective_date')
                    if edate:
                        cd['status_change_effective_date'] = None
                    continue
                elif cd.get('status_change') and required == 'newhire_rehire':
                    continue
                form = str_to_class(
                    'djpersonnel.transaction.forms', required)(
                )
                for field in form.fields:
                    cd[field] = None

        # newhire/rehire
        if cd.get('newhire_rehire'):

            # required fields for all newhire/rehire
            if employee:
                for field in REQUIRED_FIELDS_NEWHIRE[employee]:
                    if not cd.get(field):
                        self.add_error(field, "Required field")

            # newhire
            # moving expenses
            self.dependent('moving_expenses', 'Yes', 'moving_expenses_amount')

            # grant funded
            if cd.get('position_grant_funded') == 'Yes':
                for field in REQUIRED_FIELDS_GRANT_FUNDED:
                    if not cd.get(field):
                        self.add_error(field, "Required field")
            if cd.get('position_grant_funded') == 'No':
                for field in REQUIRED_FIELDS_GRANT_FUNDED:
                    cd[field] = None

            # newhire faculty
            if employee == 'faculty':

                # employment type
                contract_field = 'contract_years'
                adjunct_fields = ['courses_teaching','number_of_credits']
                graduate_fields = [
                    'academic_term','expected_end_date','food_allowance',
                    'first_seven_week_amount','second_seven_week_amount'
                ]
                et_fields = [contract_field] + adjunct_fields + graduate_fields
                et = cd.get('employment_type')
                if et:
                    # contract
                    if 'Contract' in et:
                        if not cd.get(contract_field):
                            self.add_error(contract_field, "Required field")
                        for field in adjunct_fields:
                            cd[field] = None
                        for field in graduate_fields:
                            cd[field] = None
                    # adunct
                    elif et == 'Adjunct':
                        for field in adjunct_fields:
                            self.dependent('music', 'Yes', field)
                        cd[contract_field] = None
                        for field in graduate_fields:
                            cd[field] = None
                    # graduate assistant
                    elif et == 'Graduate Assistant':
                        for field in graduate_fields:
                            if not cd.get(field):
                                self.add_error(field, "Required field")
                        cd[contract_field] = None
                        for field in adjunct_fields:
                            cd[field] = None
                    else:
                        for field in et_fields:
                            cd[field] = None

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
            if tt:
                if not cd.get('termination_{}'.format(tt.lower())):
                    self.add_error(
                        'termination_{}'.format(tt.lower()), "Please select a reason"
                    )
                    if tt == "Involuntary":
                        cd['termination_voluntary'] = None
                    else:
                        cd['termination_involuntary'] = None
            if employee == 'staff':
                field = 'vacation_days_accrued'
                if not cd.get(field):
                    self.add_error(field, "Required field")

        return cd
