from django.db import models
from django.contrib.auth.models import User
from curriculum.models import Course



# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    text = models.TextField()
    course = models.ForeignKey(Course)


class Comment(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now=True)
    