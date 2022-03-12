from django import forms
from .models import Comment
from ckeditor.fields import RichTextField


# Add your forms below
class EmailBlogPostForm(forms.Form):
    """Form for sharing posts via email"""
    name = forms.CharField(max_length=30)
    email = forms.EmailField()
    recipients = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class PostCommentForm(forms.ModelForm):
    """Form the comment section on posts"""
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


class SearchVectorForm(forms.Form):
    """Custom form for a search lookup"""
    query = forms.CharField()
