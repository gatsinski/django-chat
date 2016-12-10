from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from .views import home_page

urlpatterns = [
    url(r'^$', home_page, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^chats/', include('django_social.contrib.chats.urls', namespace='chats')),
    url(r'^users/', include('django_social.contrib.users.urls', namespace='users')),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)