# -*- coding: utf-8 -*-

from django import forms

from djpersonnel.transaction.models import Operation
from djpersonnel.core.utils import level3_choices


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
            'level3_approver','decline','email_approved'
        ]
