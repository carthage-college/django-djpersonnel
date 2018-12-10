# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm

from django.contrib.auth.models import User


class ApproverForm(forms.ModelForm):

    first_name = forms.CharField(
        max_length=30
    )
    last_name = forms.CharField(
        max_length=30
    )
    email = forms.EmailField(
        max_length=254
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class DateCreatedForm(forms.Form):

    created_at = forms.DateField(label="Created on or after")

    class Meta:
        pass
