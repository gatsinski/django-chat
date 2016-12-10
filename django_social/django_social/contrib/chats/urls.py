from django.conf.urls import url

from .views import index, load_form, send_message, load_messages

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^(?P<room_id>[0-9]+)/$', load_form, name='load_form'),
    url(r'^(?P<room_id>[0-9]+)/send/$', send_message, name='send_message'),
    url(r'^(?P<room_id>[0-9]+)/load_messages/$', load_messages, name='load_messages'),
    ]