from django import forms
from .models import Question, Option
from django.contrib.auth.forms import (UserCreationForm,
                                       AuthenticationForm,
                                       UsernameField,PasswordChangeForm,
                                       PasswordResetForm,
                                        SetPasswordForm)

from django.contrib.auth.models import User
from django.utils.translation import gettext,gettext_lazy as _


class AnswerForm(forms.Form):
    option = forms.ChoiceField(widget=forms.RadioSelect)

    def __init__(self, question, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['option'].choices = [(opt.text, opt.text) for opt in question.options.all()]

class CustomerLoginForm(AuthenticationForm):
    username=UsernameField(widget=forms.TextInput(
        attrs={'autofocus':True, 'class':'form-control'}))
    password=forms.CharField(label=_('Password'),strip=False,widget=forms.PasswordInput(
        attrs={'autocomplete':'current-password', 'class':'form-control'}))

class CustomerRegistrationForm(UserCreationForm):
    password1= forms.CharField(label='Password', 
                               widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(label='Confirm Password (again)', 
                              widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email=forms.CharField(required=True, label='Email',
                          widget=forms.EmailInput(attrs={'class':'form-control'}))
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model=User
        fields=['username','email','password1','password2']