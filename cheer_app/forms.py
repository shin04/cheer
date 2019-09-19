from django import forms
from .models import Post, Comment
from accounts.models import CustomUser as User

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text')

class SignUpForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput)
    email = forms.EmailField()
    enter_password = forms.CharField(widget=forms.PasswordInput)
    retype_password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise froms.ValidationError('The email ha been already used.')
        return email

    def clean_enter_password(self):
        password = self.cleaned_data.get('enter_password')
        if len(password) < 5:
            raise forms.ValidationError('Password must contain 5 or more characters.')
        return password

    def clean(self):
        super(SignUpForm, self).clean()
        password = self.cleaned_data.get('enter_password')
        retyped = self.cleaned_data.get('retype_password')
        if password and retyped and (password != retyped):
            self.add_error('retype_password', 'This does not match with the above.')

    def save(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('enter_password')
        email = self.cleaned_data.get('email')
        new_user = User.objects.create_user(username = username, email=email)
        new_user.set_password(password)
        new_user.save()
