from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import User


class RegisterForm(forms.ModelForm):
    password_repeat = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name',)
        widgets = {'password': forms.PasswordInput}

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get('password')
        password_repeat = cleaned_data.get('password_repeat')
        if password != password_repeat:
            message = _('The passwords does not match')
            self.add_error('password', message)
            self.add_error('password_repeat', message)
        return cleaned_data

    def save(self, commit=True):
        instance = super(RegisterForm, self).save(commit=False)
        if commit:
            User.objects.create_user(instance.username,
                                     instance.email,
                                     instance.password,
                                     first_name=instance.first_name,
                                     last_name=instance.last_name)
        return instance


class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {'password': forms.PasswordInput}
