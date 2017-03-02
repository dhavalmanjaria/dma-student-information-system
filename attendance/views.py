from django.shortcuts import render
from django.views import generic
from .models import Attendance


class AttendanceList(generic.ListView):
    model = Attendance

