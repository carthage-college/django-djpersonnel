# -*- coding: utf-8 -*-

from django import forms
from djpersonnel.finance.budget.models import Budget


class BudgetForm(forms.ModelForm):
    """Form class for the budget data model."""

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
            'denied',
            'denied_date',
        ]

    def dependent(self, field1, field2, value=None):
        """Deal with dependent fields."""
        cd = self.cleaned_data

        if cd.get(field1) == value and not cd.get(field2):
            self.add_error(field2, "Required field")
        elif cd.get(field1) != value:
            cd[field2] = None

    def clean(self):
        """Form validation."""
        cd = self.cleaned_data
        self.dependent('change_type', 'useful_life', 'Capital')
        self.dependent('variation', 'variation_from', 'Transfer to or from')
        self.dependent('variation', 'variation_to', 'Transfer to or from')
        self.dependent('variation', 'variation_change', 'Increase to budget')
        self.dependent('variation', 'variation_change', 'Decrease to budget')

        return cd
