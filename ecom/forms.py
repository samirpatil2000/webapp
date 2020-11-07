from django import forms
from .models import Address
from django.core.validators import MinValueValidator,MaxValueValidator

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

class UpdateAddress(forms.ModelForm):
    class Meta:
        model=Address
        fields=['name',
                'address_1',
                'address_2',
                'mobile_number',
                'zipcode',
                'city',
                'is_save',
                ]

    def save(self, commit=True):
        addr=self.instance
        addr.name=self.cleaned_data['name']
        addr.address_1=self.cleaned_data['address_1']
        addr.address_2=self.cleaned_data['address_2']
        addr.mobile_number=self.cleaned_data['mobile_number']
        addr.zipcode=self.cleaned_data['zipcode']
        addr.city=self.cleaned_data['city']
        addr.is_save=self.cleaned_data['is_save']

        if commit:
            addr.save()
        return addr


PAYMENT_CHOICES = (
    ('P', 'PayTm'),
    ('S', 'Stripe'),
    ('C', 'Cash On Delivery'),
)

class ChechoutForm(forms.Form):
    name=forms.CharField(required=True)
    address_1=forms.CharField(required=True)
    address_2=forms.CharField(required=False)
    mobile_number=forms.IntegerField(required=True)
    zipcode=forms.IntegerField(required=True,validators=[MinValueValidator(99999),MaxValueValidator(999999)])
    city=forms.CharField(required=True)
    is_save=forms.BooleanField(required=False)
    payment_option=forms.ChoiceField(widget=forms.RadioSelect,
                                      choices=PAYMENT_CHOICES)

class ChechoutFormPaymentOption(forms.Form):
    payment_option = forms.ChoiceField(widget=forms.RadioSelect,
                                       choices=PAYMENT_CHOICES)