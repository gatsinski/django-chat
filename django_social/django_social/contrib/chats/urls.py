from django.conf.urls import url

from .views import index, load_form, send_message, sync_messages, get_previous

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^(?P<room_id>[0-9]+)/$', load_form, name='load_form'),
    url(r'^(?P<room_id>[0-9]+)/send/$', send_message, name='send_message'),
    url(r'^(?P<room_id>[0-9]+)/sync/$', sync_messages, name='sync_messages'),
    url(r'^(?P<room_id>[0-9]+)/get_previous/$', get_previous, name='get_previous'),
    ]