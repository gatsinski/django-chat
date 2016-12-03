import datetime

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Message, Room


class ChatForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ('message','file')

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.author = self.user
        self.room.say(instance.author, instance.message, instance.file)
        return instance
