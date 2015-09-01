from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'app.views.home', name="home"),

    #USER HANDLING
    url(r'^register/$', 'app.views.register', name='register'),
    url(r'^register_success/', ('app.views.register_confirmation'), name='success'),
    url(r'^register/confirm/expired', ('app.views.confirm_expired')),
    url(r'^register/confirm/(?P<activation_key>\w+)/', ('app.views.register_confirm')),
    url(r'^register_confirmation/', ('app.views.register_confirm_mail')),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^accounts/profile/$', 'app.views.profile', name='profile'),
    url(r'^profile/$', 'app.views.profile', name='profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)