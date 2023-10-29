from typing import Any
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import Task

User = get_user_model()


class RegisterForm(UserCreationForm):
    # email = forms.EmailField(label="Your Email")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True

    class Meta:
        model = User
        fields = [
            'username',
            'email'
        ]


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)

    def clean(self):
        cd = self.cleaned_data
        # self.add_error("password", "Invalid Password")
        # raise forms.ValidationError("Invalid value: %(value)s", code="invalid", params={"value": 100})
        # raise forms.ValidationError([
        #     forms.ValidationError("error 1", code="invalid 1"), 
        #     forms.ValidationError("error 2", code="invalid 2")
        # ])
        raise forms.ValidationError({
            "password": forms.ValidationError("Invalid Password", code="invalid_password")
        })
        

class UpdateTaskForm(forms.ModelForm):

    class Meta:
        model = Task
        # fields = "__all__"
        fields = [
            "title",
            "description",
            "status",
            "due_date",
            "due_time"
        ]



