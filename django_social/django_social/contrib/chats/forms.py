import datetime

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Message


class ChatForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ('message',)