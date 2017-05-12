from django.shortcuts import render, redirect
from .models import MeetingMinute, Meeting
from django.contrib.auth.decorators import (
    login_required, permission_required)
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin)
from django.views.generic import ListView
from datetime import datetime
from .forms import MeetingForm, MeetingMinuteForm


class ListMeetings(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Meeting
    paginate_by = 10
    template_name = 'meeting-details/all-meetings.html'

    permission_required = 'user_management.can_read_meeting_details'


@login_required
@permission_required('user_management.can_write_meeting_details')
def edit_meeting(request, meeting_pk):
    context = {}

    meeting = Meeting.objects.get(pk=meeting_pk)
    meeting_minutes = MeetingMinute.objects.filter(meeting=meeting)
    
    meeting_minute_form = MeetingMinuteForm()
    meeting_form = MeetingForm()

    if request.method == "POST":
        meeting_minute_form = MeetingMinuteForm(request.POST)
        submit = request.POST.get('submit')

        if submit == "Add New":
            if meeting_minute_form.is_valid():
                text = meeting_minute_form.cleaned_data['text']

                meeting_minute = MeetingMinute(text=text)

                meeting_minute.meeting = meeting

                meeting_minute.save()
                context['success'] = True
                # return redirect('edit-meeting', meeting_pk=meeting.pk)
            else:
                context['success'] = False

        if submit == "Save":
            if meeting_minute_form.is_valid():
                meeting_minute = MeetingMinute.objects.get(
                    pk=request.POST.get('meeting_minute_pk'))

                meeting_minute.text = meeting_minute_form.cleaned_data['text']

                meeting_minute.save()
                context['success'] = True
                # return redirect('edit-meeting', meeting_pk=meeting.pk)
            else:
                context['success'] = False

        if submit == "Delete":
            meeting_minute = MeetingMinute.objects.get(
                    pk=request.POST.get('meeting_minute_pk'))

            meeting_minute.delete()

        # Meeting Information saved here
        if submit == "Save Info":

            meeting_form = MeetingForm(request.POST)
            if meeting_form.is_valid():
                agenda = meeting_form.cleaned_data['agenda']
                participants = meeting_form.cleaned_data['participants']
                description = meeting_form.cleaned_data['description']
                date = meeting_form.cleaned_data['date']

                hours = request.POST.get('hours')
                minutes = request.POST.get('minutes')
                ampm = request.POST.get('a')

                meeting_time = datetime.strptime(
                    hours + " " + minutes + " " + ampm, "%I %M %p")

                meeting = Meeting.objects.get(
                    pk=request.POST.get('meeting_pk'))

                meeting.agenda = agenda
                meeting.participants = participants
                meeting.description = description
                meeting.date = date
                meeting.time = meeting_time

                meeting.save()

                context['success'] = True
                # return redirect('edit-meeting', meeting_pk=meeting.pk)
            else:
                context['success'] = False

    context['meeting'] = meeting
    context['meeting_minutes'] = meeting_minutes
    context['current_date'] = datetime.now().date()

    context['meeting_form'] = meeting_form
    context['meeting_minute_form'] = meeting_minute_form

    return render(request, 'meeting-details/edit-meeting.html', context)


@login_required
@permission_required('user_management.can_write_meeting_details')
def create_meeting(request):
    context = {}

    meeting_form = MeetingForm()

    if request.method == "POST":

        meeting_form = MeetingForm(request.POST)
        if meeting_form.is_valid():
            agenda = meeting_form.cleaned_data['agenda']
            participants = meeting_form.cleaned_data['participants']
            description = meeting_form.cleaned_data['description']
            date = meeting_form.cleaned_data['date']

            hours = request.POST.get('hours')
            minutes = request.POST.get('minutes')
            ampm = request.POST.get('a')

            meeting_time = datetime.strptime(
                hours + " " + minutes + " " + ampm, "%I %M %p")

            meeting = Meeting()

            meeting.agenda = agenda
            meeting.participants = participants
            meeting.description = description
            meeting.date = date
            meeting.time = meeting_time

            meeting.save()

            context['success'] = True
            return redirect('edit-meeting', meeting_pk=meeting.pk)
        else:
            context['success'] = False

    return render(request, 'meeting-details/create-meeting.html', context)


@login_required
@permission_required('user_management.can_read_meeting_details')
def view_meeting(request, meeting_pk):
    context = {}

    context['meeting'] = Meeting.objects.get(pk=meeting_pk)
    context['meeting_minutes'] = MeetingMinute.objects.filter(
        meeting__pk=meeting_pk)

    return render(request, 'meeting-details/view-meeting.html', context)
