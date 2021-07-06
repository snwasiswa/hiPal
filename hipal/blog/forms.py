from django import forms


# Add your forms below
class EmailBlogPostForm(forms.Form):
    """Form for sharing posts via email"""
    name = forms.CharField(max_length=30)
    email = forms.EmailField()
    recipients = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)
