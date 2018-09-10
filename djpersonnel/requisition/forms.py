# -*- coding: utf-8 -*-

from django import forms

from djpersonnel.requisition.models import Operation
from djpersonnel.core.utils import _level3_choices

from djtools.fields import BINARY_CHOICES


class OperationForm(forms.ModelForm):

    applicant_system = forms.ChoiceField(
        label="""
            Would you like any others to have access to the
            applications in the Applicant Pro system?
        """,
        choices=BINARY_CHOICES, widget=forms.RadioSelect()
    )
    new_position = forms.ChoiceField(
        label="Is this a new position?",
        choices=BINARY_CHOICES, widget=forms.RadioSelect()
    )
    level3 = forms.ChoiceField(
        label="Who will approve this request for you?",
        choices=_level3_choices()
    )

    class Meta:
        model = Operation
        # either fields or exclude is required
        exclude = [
            'created_by','updated_by','created_at','updated_at',
            'level1,level1_date','level2,level2_date','level3,level3_date',
            'decline','email_approved'
        ]


    def clean_replacement_name(self):

        cd = self.cleaned_data
        if cd.get('new_position') == 'No' and not cd.get('replacement_name'):
            raise forms.ValidationError("You must provide a replacement name.")

        return cd['replacement_name']

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
