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
        ]
