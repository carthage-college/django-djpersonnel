# -*- coding: utf-8 -*-

from django import forms

class DateCreatedForm(forms.Form):

    created_at = forms.DateField(label="Created on or after")

    class Meta:
        pass
