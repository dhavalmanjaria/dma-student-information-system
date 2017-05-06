from django.shortcuts import render
from django.urls import reverse_lazy
from actions.views import SelectCourseSemester
from actions.forms import SelectSemesterForm
from curriculum.models import Semester
from django.views.generic import ListView
from .models import FeeCollection, Payment
from .forms import PaymentForm
from datetime import datetime
import logging

LOG = logging.getLogger('app')


class SelectFee(SelectCourseSemester):
    """
    Select course and semester to select studens for.
    """
    form = SelectSemesterForm
    select_template = 'fee-management/select-fees.html'
    redirect_to = 'all-fees'
    context = {}


class FeeCollectionsList(ListView):
    model = FeeCollection

    template_name = 'fee-management/all-fees.html'

    def get(self, request, semester_pk, *args, **kwargs):
        self.semester = Semester.objects.get(pk=semester_pk)

        return super(FeeCollectionsList, self).get(request, semester_pk)

    def get_queryset(self):
        return FeeCollection.objects.filter(student__semester=self.semester)


def add_payment(request, std_pk):
    context = {}

    fee_collection = FeeCollection.objects.filter(student__pk=std_pk).first()

    payments = Payment.objects.filter(student_fee=fee_collection).order_by(
        '-date')


    if request.method == "POST":
        form = PaymentForm(request.POST)

        if form.is_valid():
            fee_collection= form.cleaned_data['student_fee']
            amount_paid = form.cleaned_data['amount']

            fee_collection.pending_amount = fee_collection.pending_amount - amount_paid
            fee_collection.save()

            new_payment = Payment(
                student_fee=fee_collection, amount=amount_paid)

            new_payment.save()
            context['success'] = True
        else:
            context['success'] = False

    context['payments'] = payments
    context['fee_collection'] = fee_collection
    context['current_date'] = datetime.now().date()
    context['form'] = PaymentForm()

    return render(request, 'fee-management/add-payment.html', context)
