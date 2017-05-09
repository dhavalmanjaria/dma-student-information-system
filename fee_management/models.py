from django.db import models
from user_management.models.group_info import StudentInfo


class FeeItem(models.Model):
    """
    Represents a pre-specified amount that can be added
    to a student's total fees
    """
    item_name = models.CharField(
        max_length=200, help_text='Name of the fee item with a fixed amount')
    item_amount = models.PositiveIntegerField()


class FeeCollection(models.Model):
    """
    Represents the total amount of fees a student has yet to pay
    """
    student = models.OneToOneField(StudentInfo)
    pending_amount = models.PositiveIntegerField()
    fee_items = models.ManyToManyField(FeeItem)


class Payment(models.Model):
    """
    Represents a payment made by a student towards the completion of their fees
    """
    student_fee = models.ForeignKey(FeeCollection)
    date = models.DateField(auto_now=True)
    amount = models.PositiveIntegerField()
