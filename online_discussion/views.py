from django.shortcuts import render, redirect
from .models import Post, Comment
from user_management.models.group_info import FacultyInfo, StudentInfo
from .forms import CreatePostForm, NewCommentForm
from django.contrib.auth.models import Permission
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from curriculum.models import Course
from datetime import datetime
import logging

LOG = logging.getLogger('app')


def view_posts(request):
    context = {}

    user = request.user

    course = None
    # User is a faculty
    if FacultyInfo.objects.filter(user=user).first():
        course = user.facultyinfo.course

    # User is a student
    if StudentInfo.objects.filter(user=user).first():
        course = user.studentinfo.semester.course

    posts = Post.objects.filter(course=course)

    # User is UpperManagement
    if user.has_perm('user_management.can_auth_FacultyHOD'):
        posts = Post.objects.all()
        course = "All Courses"
        context['courses'] = Course.objects.all()

    # Paginator
    posts_page = posts

    page = request.GET.get('page', 1)

    paginator = Paginator(posts_page, 10)  # number is no. of posts per page

    try:
        posts_page = paginator.page(page)
    except PageNotAnInteger:
        posts_page = paginator.page(1)  # First page
    except EmptyPage:
        posts_page = paginator.page(paginator.num_pages)  # Last page

    context['posts_page'] = posts_page

    context['umperm'] = Permission.objects.get(codename='can_auth_FacultyHOD')
    
    context['posts'] = posts

    context['course'] = course

    return render(
        request, 'online-discussion/view-posts.html', context)


@login_required
@permission_required('user_management.can_read_online_discussion')
def create_post(request, course_pk):
    context = {}

    course = Course.objects.get(pk=course_pk)

    form = CreatePostForm()

    context['form'] = form
    context['course'] = course

    if request.method == "POST":
        form = CreatePostForm(request.POST)

        if form.is_valid():
            post = Post()
            post.title = form.cleaned_data['title']
            post.text = form.cleaned_data['text']
            post.user = request.user
            post.course = course

            post.save()

        return redirect('view-posts')

    return render(request, 'online-discussion/create-post.html', context)


@login_required
@permission_required('user_management.can_write_online_discussion')
def post_comments(request, post_pk):
    context = {}
    context['umperm'] = Permission.objects.get(codename='can_auth_FacultyHOD')
    
    if request.method == "POST":
        post_pk = request.POST.get('post_pk')
        post = Post.objects.get(pk=post_pk)
        form = NewCommentForm(request.POST)

        if form.is_valid():
            LOG.debug('form is valid')
            new_comment = Comment(post=post)
            new_comment.text = form.cleaned_data['text']
            new_comment.user = request.user

            new_comment.save()

            return redirect('post-comments', post_pk=post.pk)
        else:
            LOG.debug(form.errors)

    post = Post.objects.get(pk=post_pk)

    comments = Comment.objects.filter(post=post)

    context['comments'] = comments
    context['post'] = post


    return render(
        request, 'online-discussion/post-comments.html', context)


@login_required
@permission_required('user_management.can_write_online_discussion')
def edit_post(request, post_pk):
    context = {}

    post = Post.objects.get(pk=post_pk)
    form = CreatePostForm(initial={'title': post.title, 'text': post.text})

    if request.user != post.user:
        raise PermissionDenied

    if request.method == "POST":
        form = CreatePostForm(request.POST)

        if form.is_valid():
            post_pk = request.POST.get('post_pk')
            post = Post.objects.get(pk=post_pk)
            post.title = form.cleaned_data['title']
            post.text = form.cleaned_data['text']

            post.date_updated = datetime.now()

            post.save()

            return redirect('post-comments', post_pk=post.pk)


    context['form'] = form
    context['post'] = post

    return render(
        request, 'online-discussion/edit-post.html', context)