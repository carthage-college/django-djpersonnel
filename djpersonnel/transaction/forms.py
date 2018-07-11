# -*- coding: utf-8 -*-

from django import forms

from djpersonnel.action.models import Operation

class OperationForm(forms.ModelForm):

    class Meta:
        model = Operation
        # either fields or exclude is required
        fields = '__all__'

