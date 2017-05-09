from django.shortcuts import render
from django.urls import reverse_lazy
from actions.views import SelectCourseSemester
from actions.forms import SelectSemesterForm
from curriculum.models import Semester
from django.views.generic import ListView
from .models import FeeCollection, Payment, FeeItem
from .forms import PaymentForm, AmountPendingForm, FeeItemForm
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

    form = PaymentForm()
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
    context['form'] = form

    return render(request, 'fee-management/add-payment.html', context)


def edit_fees(request, std_pk):
    context = {}

    fee_collection = FeeCollection.objects.filter(student__pk=std_pk).first()
    all_fee_items = set(FeeItem.objects.all())

    form = AmountPendingForm()

    if request.method == "POST":
        form = AmountPendingForm(request.POST)
        if form.is_valid():
            amount_pending = form.cleaned_data['pending_amount']

            # I realise I made a stupid mistake here that is going to bite me
            # in the future. So, sorry, future me.
            fee_collection.pending_amount = amount_pending
            fee_collection.save()

            context['success'] = True
        else:
            context['success'] = False

    context['all_fee_items'] = all_fee_items
    context['fee_collection'] = fee_collection
    context['form'] = form

    return render(request, 'fee-management/edit-fees.html', context)


def edit_fee_items(request):
    context = {}
    context['fee_items'] = FeeItem.objects.all().order_by('item_name')

    form = FeeItemForm()

    if request.method == "POST":
        form = FeeItemForm(request.POST)

        submit = request.POST.get('submit')

        if submit == "Add New":
            if form.is_valid():
                item_name = request.POST.get('item_name')
                item_amount = request.POST.get('item_amount')

                fee_item = FeeItem(
                    item_name=item_name, item_amount=item_amount)

                fee_item.save()

                context['success'] = True
            else:
                context['success'] = False

        if submit == "Save":
            if form.is_valid():
                fee_item_pk = request.POST.get('fee_item_pk')
                item_name = request.POST.get('item_name')
                item_amount = request.POST.get('item_amount')

                fee_item = FeeItem.objects.get(pk=fee_item_pk)

                fee_item.item_name = item_name
                fee_item.item_amount = item_amount
                fee_item.save()

                context['success'] = True
            else:
                context['success'] = False

        if submit == "Delete":
            if form.is_valid():
                fee_item_pk = request.POST.get('fee_item_pk')
                fee_item = FeeItem.objects.get(pk=fee_item_pk)
                fee_item.delete()

        context['form'] = form

    return render(request, 'fee-management/edit-fee-items.html', context)
