from django import forms
from localflavor.gb.forms import GBPostcodeField
from .models import Order


class OrderCreateForm(forms.ModelForm):
    postal_code = GBPostcodeField()
    class Meta:
        model = Order
        fields = [
            'first_name',
            'last_name',
            'email',
            'address',
            'postal_code',
            'city'
        ]