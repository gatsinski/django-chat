from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^chats/', include('django_social.contrib.chats.urls', namespace='chats')),
    url(r'^users/', include('django_social.contrib.users.urls', namespace='users')),
]
