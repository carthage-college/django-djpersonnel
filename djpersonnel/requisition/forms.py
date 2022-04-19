# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User

from djpersonnel.requisition.models import Operation
from djpersonnel.core.utils import level3_choices

from djtools.fields import BINARY_CHOICES


class OperationForm(forms.ModelForm):


    applicant_system = forms.ChoiceField(
        label="""
            Would you like any others to have access to the
            applications in the Applicant Pro system? (Search Committee)
        """,
        choices=BINARY_CHOICES, widget=forms.RadioSelect()
    )
    new_position = forms.ChoiceField(
        label="Is this a new position?",
        choices=BINARY_CHOICES, widget=forms.RadioSelect()
    )

    def __init__(self, *args, **kwargs):
        super(OperationForm, self).__init__(*args, **kwargs)
        self.fields['level3_approver'] = forms.ChoiceField(
            label="Who will approve this request for you?",
            choices=level3_choices()
        )

    class Meta:
        """Sub-class with settings for the parent class."""

        model = Operation
        exclude = [
            'created_by',
            'updated_by',
            'created_at',
            'updated_at',
            'level1',
            'level1_date',
            'level2',
            'level2_date',
            'level3',
            'level3_date',
            'decline',
            'email_approved',
        ]

    def clean_replacement_name(self):

        cd = self.cleaned_data
        if cd.get('new_position') == 'No' and not cd.get('replacement_name'):
            raise forms.ValidationError("You must provide a replacement name.")

        return cd['replacement_name']

    def clean_hours_per_week(self):

        cd = self.cleaned_data
        if cd.get('salary_type') == 'Non-exempt' and not cd.get('hours_per_week'):
            raise forms.ValidationError("You must provide hours per week.")

        return cd['hours_per_week']

    def clean_account_number(self):

        cd = self.cleaned_data
        if cd.get('budgeted_position') == 'Yes' and not cd.get('account_number'):
            raise forms.ValidationError("You must provide an account number.")

        return cd['account_number']

    def clean_grant_fund_amount(self):

        cd = self.cleaned_data
        if cd.get('position_grant_funded') == 'Yes' and not cd.get('grant_fund_amount'):
            raise forms.ValidationError("You must provide a percentage or amount.")

        return cd['grant_fund_amount']

    def clean_applicant_system_people(self):

        cd = self.cleaned_data
        if cd.get('applicant_system') == 'Yes' and \
          not cd.get('applicant_system_people'):
            raise forms.ValidationError(("You must provide the names of those "
                "who will have access to the Applicant Pro system."))

        return cd['applicant_system_people']

    def clean_speciality_sites_urls(self):

        cd = self.cleaned_data
        if cd.get('speciality_sites') == 'Yes' and \
          not cd.get('speciality_sites_urls'):
            raise forms.ValidationError(("You must provide the URL(s) for "
                "the speciality site(s)."))

        return cd['speciality_sites_urls']

    def clean_level3_approver(self):
        cd = self.cleaned_data
        approver = cd.get('level3_approver')

        if approver:
            cd['level3_approver'] = User.objects.get(username=approver)
        else:
            cd['level3_approver'] = None

        #return cd
        return cd['level3_approver']
