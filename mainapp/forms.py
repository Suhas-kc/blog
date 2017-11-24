from django import forms
from .models import User,BlogPost,CommentPost,Tag

class userForm(forms.ModelForm):
    """
    ModelForm to collect data for model User
    """
    class Meta:
        model = User
        fields = ['username','email','password','first_name','last_name'] #Copy the email to username in views later
        widgets = {
            'password' : forms.PasswordInput,
        }

    def clean_username(self):
        """
        Validation function to check if username has already been used
        """
        data = self.cleaned_data['username']
        try:
            checkUser = User.objects.get(username=data)
            if checkUser is not None:
                raise forms.ValidationError("Username is already taken")

        except User.DoesNotExist:
            return data


class loginForm(forms.Form):
    """
    Form for login information
    """
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput,required=True)

class submitBlogForm(forms.ModelForm):
    tags = forms.ModelChoiceField(Tag.objects.all(),required=True)
    class Meta:
        model = BlogPost
        fields = ['title','content','tags']

class submitCommentForm(forms.ModelForm):
    class Meta:
        model = CommentPost
        fields = ['content']
        labels = {
            'content' : 'Reply',
        }