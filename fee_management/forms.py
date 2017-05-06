from django import forms
from .models import FeeCollection, Payment


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
