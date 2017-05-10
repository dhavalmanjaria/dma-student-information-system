from django.shortcuts import render, redirect
from django.contrib.auth.decorators import (
    login_required, permission_required)
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin)
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from actions.views import SelectCourseSemester
from .forms import SelectBookStudentForm
from .models import Book
from user_management.models.group_info import StudentInfo
import logging

LOG = logging.getLogger('app')


def all_books(request):
    context = {}

    context['books'] = Book.objects.all().order_by('title')
    return render(request, 'library-management/all-books.html', context)


class SelectBookStudent(LoginRequiredMixin,
                        PermissionRequiredMixin, SelectCourseSemester):

    form = SelectBookStudentForm
    select_template = 'library-management/select-book-student.html'
    redirect_to = 'set-book-user'
    context = {}

    permission_required = 'user_management.can_read_pass_my_book'

    def get(self, request, book_pk):

        book_pk = self.kwargs['book_pk']
        book = Book.objects.get(pk=book_pk)
        self.context['book'] = book

        return super(SelectBookStudent, self).get(request)


    # def get_context_data(self, **kwargs):
    #     LOG.debug(self.context)
    #     self.context = super(
    #         SelectBookStudent, self).get_context_data(**kwargs)
        
    #     self.context['book'] = book
    #     return self.context

    def post(self, request, book_pk):
        form = SelectBookStudentForm(request.POST)

        if form.is_valid():
            book_pk = form.cleaned_data['book_pk']
            semester = form.cleaned_data['semester']
            return redirect(self.redirect_to, semester.pk, book_pk)
        else:
            self.context = {}
            self.context['errors'] = True
            self.context['form'] = form
        return render(request, self.select_template, self.context)


@login_required
@permission_required('user_management.can_read_pass_my_book')
def set_book_user(request, sem_pk, book_pk):
    context = {}
    context['students'] = StudentInfo.objects.filter(semester__pk=sem_pk)
    book = Book.objects.get(pk=book_pk)
    context['book'] = book

    if request.method == "POST":
        std_pk = request.POST.get('std_pk')

        student = StudentInfo.objects.get(pk=std_pk)

        book.student = student

        book.save()

    return render(request, 'library-management/set-book-user.html', context)


class CreateBook(LoginRequiredMixin,
                 PermissionRequiredMixin, CreateView):
    model = Book
    permission_required = 'user_management.can_read_pass_my_book'
    success_url = reverse_lazy('all-books')
    template_name = 'library-management/create-book.html'
    fields = (('title'), )


class UpdateBook(LoginRequiredMixin,
                 PermissionRequiredMixin, UpdateView):
    model = Book
    permission_required = 'user_management.can_read_pass_my_book'
    success_url = reverse_lazy('all-books')
    template_name = 'library-management/update-book.html'
    fields = (('title'), ('due_date'))


class DeleteBook(LoginRequiredMixin,
                 PermissionRequiredMixin, DeleteView):
    model = Book
    permission_required = 'user_management.can_read_pass_my_book'
    success_url = reverse_lazy('all-books')
