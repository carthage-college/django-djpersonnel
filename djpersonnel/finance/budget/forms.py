# -*- coding: utf-8 -*-

from django import forms
from djpersonnel.finance.budget.models import Budget
from djpersonnel.finance.budget.models import VARY_CHOICES
from djpersonnel.core.utils import level3_choices


class BudgetForm(forms.ModelForm):
    """Form class for the budget data model."""

    #variation = forms.ChoiceField(
        #label="Is this an increase or decrease in the budget amount?",
        #choices=VARY_CHOICES,
        #widget=forms.RadioSelect(),
        #required=True,
    #)

    def __init__(self, *args, **kwargs):
        super(BudgetForm, self).__init__(*args, **kwargs)
        self.fields['approver'] = forms.ChoiceField(
            label="Who will approve this request for you?",
            choices=level3_choices(),
        )

    class Meta:
        """Sub-class with settings for the parent class."""

        model = Budget
        exclude = [
            'created_by',
            'updated_by',
            'created_at',
            'updated_at',
            'approved',
            'approved_date',
            'decline',
        ]

    #def clean_variation(self):
        #"""Required field that is not handled properly."""
        #cd = self.cleaned_data
        #if not cd['variation']:
            #self.add_error('variation', "Required field")
        #return cd
