from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms
from .models import Task

User = get_user_model()


class RegistrationForm(UserCreationForm):
    # email = forms.EmailField(label="Your Email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = [
            'username',
            'email'
        ]


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)

    # def clean(self):
    #     cd = self.cleaned_data
    #     if cd.get('password') != cd.get('password_confirm'):
    #         self.add_error('password_confirm', "passwords do not match !")
    #     return cd


class UpdateTaskForm(forms.ModelForm):

    class Meta:
        model = Task
        # fields = '__all__'
        fields = [
            'title',
            'description',
            'status',
            'due_date',
            'due_time'
        ]
