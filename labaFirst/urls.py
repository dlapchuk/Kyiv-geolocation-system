from django.conf.urls import patterns, include, url
from django.contrib import admin
from dbSearch import views
import dbSearch.urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'labaFirst.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^dbSearch/',include('dbSearch.urls')),

    url(r'^',views.outFacts),
)
