# -*- coding: utf-8 -*-

from django import forms

from djpersonnel.requisition.models import Operation

class OperationForm(forms.ModelForm):

    class Meta:
        model = Operation
        # either fields or exclude is required
        fields = '__all__'

