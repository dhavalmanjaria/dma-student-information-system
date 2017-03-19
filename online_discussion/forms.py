from django import forms
from .models import Post, Comment


class CreatePostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text')


class NewCommentForm(forms.ModelForm):
    """
    This form is only used to generate a cleaned_data[] value for the comment
    text
    """
    class Meta:
        model = Comment
        fields = ('text', )
