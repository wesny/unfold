from django import forms
from django.db import models
from unfold.transactions.models import Purchase

class PurchaseForm(forms.Form):

    price = forms.DecimalField(max_digits=8, decimal_places=2, widget=forms.HiddenInput())
    external_id = forms.CharField(max_length=255, widget=forms.HiddenInput())
    publisher = forms.CharField(max_length=255, widget=forms.HiddenInput())

    def validate(self):
        if self.has_changed():
            raise forms.ValidationError('Form fields cannot change.')
        return self.cleaned_data

