from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    def add_message(self, type, sender, message=None):
        '''Generic function for adding a message to the chat room'''
        m = Message(room=self, type=type, author=sender, message=message)
        m.save()
        return m

    def say(self, sender, message):
        '''Say something in to the chat room'''
        return self.add_message('m', sender, message)

    def join(self, user):
        '''A user has joined'''
        return self.add_message('j', user)

    def leave(self, user):
        '''A user has leaved'''
        return self.add_message('l', user)

    def messages(self, after_pk=None, after_date=None):
        '''List messages, after the given id or date'''
        m = Message.objects.filter(room=self)
        if after_pk:
            m = m.filter(pk__gt=after_pk)
        if after_date:
            m = m.filter(timestamp__gte=after_date)
        return m.order_by('pk')

    def last_message_id(self):
        '''Return last message sent to room'''
        m = Message.objects.filter(room=self).order_by('-pk')
        if m:
            return m[0].id
        else:
            return 0

    def __str__(self):
        return self.description or "Chat room %d" % self.pk

    def get_description(self):
        return self.__str__()


class Message(models.Model):
    '''A message that belongs to a chat room'''

    MESSAGE_TYPE_CHOICES = (
        ('s', 'system'),
        ('a', 'action'),
        ('m', 'message'),
        ('j', 'join'),
        ('l', 'leave'),
        ('n', 'notification')
    )

    room = models.ForeignKey(Room)
    type = models.CharField(max_length=1, choices=MESSAGE_TYPE_CHOICES)
    author = models.ForeignKey(User, related_name='author', blank=True, null=True)
    message = models.CharField(max_length=255, blank=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.type == 's':
            return u'SYSTEM: %s' % self.message
        elif self.type == 'n':
            return u'NOTIFICATION: %s' % self.message
        elif self.type == 'j':
            return 'JOIN: %s' % self.author
        elif self.type == 'l':
            return 'LEAVE: %s' % self.author
        elif self.type == 'a':
            return 'ACTION: %s > %s' % (self.author, self.message)
        return self.message
