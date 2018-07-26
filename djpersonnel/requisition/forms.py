# -*- coding: utf-8 -*-

from django import forms

from djpersonnel.requisition.models import Operation

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

    class Meta:
        model = Operation
        # either fields or exclude is required
        exclude = [
            'created_by','updated_by','created_at','updated_at',
            'level1,level1_date','level2,level2_date','level3,level3_date',
            'decline','email_approved'
        ]

    def clean_replacement_name(self):

        if self.cleaned_data.get('new_position') == "No" \
          and not self.cleaned_data.get('replacement_name'):
            raise forms.ValidationError("You must provide a replacement name.")

        return self.cleaned_data['replacement_name']
