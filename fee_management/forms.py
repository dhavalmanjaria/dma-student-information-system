from django import forms
from .models import FeeCollection, Payment, FeeItem


class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = '__all__'

    def clean_amount(self):
        data = self.cleaned_data['amount']
        student_fee = self.cleaned_data['student_fee']

        if data > student_fee.pending_amount:
            raise forms.ValidationError(
                "Amount entered is greater than pending amount")

        return data


class AmountPendingForm(forms.ModelForm):

    class Meta:
        model = FeeCollection
        fields = (('pending_amount'),)


class FeeItemForm(forms.ModelForm):

    class Meta:
        model = FeeItem
        fields = (('item_name'), ('item_amount'))
