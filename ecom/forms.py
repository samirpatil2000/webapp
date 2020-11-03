from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model=Address
        fields=['name',
                'address_1',
                'address_2',
                'mobile_number',
                'zipcode',
                'city',
                'is_save',]