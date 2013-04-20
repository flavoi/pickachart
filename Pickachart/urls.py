from django.conf.urls.defaults import *
from django.conf import settings

# Attivazione Admin
from django.contrib import admin
admin.autodiscover()

# Generale
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

# App auth
urlpatterns += patterns('auth',
    url(r'login/$', 'views.login', {'template_name':'login.html'}, name="login"),
    url(r'logout/$', 'views.logout_then_login', {'login_url':'login'}, name="logout"),
)

# App core
urlpatterns += patterns('core',
    url(r'^$', 'views.create_chart', name="main-view"),
    url(r'^home/$', 'views.create_chart', name="home"),
    url(r'^home/popola_grafico/(?P<id>\d{0,4})/(?P<idupdate>\d{1,4})/$', 'views.define_data', name="defdata"),
    url(r'^home/visualizza/(?P<id>\d{0,4})/(?P<style>[a-z,_]{0,30})/$', 'views.visualize_chart', name="visualize"),
    url(r'^home/modifica/(\d{0,4})/$', 'views.create_chart', name="update"),
    url(r'^home/riepilogo/$', 'views.viewall', name="allcharts"),
)

if settings.DEBUG == True:
    # Supporto a MEDIA_ROOT e JQUERY_ROOT (solo in sviluppo)
    urlpatterns += patterns('',
        url(r'^uploaded/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),
        url(r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT + 'js/',}),
    )
