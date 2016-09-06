from django.conf.urls import patterns, url

from dbSearch import views

urlpatterns = patterns('',

    ##############################

    #url(r'^filldb/',views.index),
    url(r'^outFacts/',views.outFacts),
    url(r'^addFact/confirm/',views.addFactConfirm),
    url(r'^addFact/',views.addPlace),
    url(r'^editFact/confirm/',views.editFactConfirm),
    url(r'^editFact/',views.editFact),
    url(r'^deleteFact/',views.deleteFact),
    url(r'^showFact/',views.showFact),
    url(r'^markStat/',views.custStat),
    url(r'^favorite/',views.favorite),
    url(r'^login/',views.login),
    url(r'^logout/',views.logout),
    url(r'^signin/',views.signin),
    url(r'^addFavorite/',views.addFavorite),
    url(r'^deleteFavorite/',views.deleteFavorite),
    url(r'^/dbSearch/favorite/showFact/', views.showFact),
    #url(r'^/dbSearch/finder/showFact/', views.showFact),
    url(r'^finder/', views.finder),
    url(r'^page/(\d+)/$', views.outFacts),
    url(r'^makeDump/',views.makeDump),
    url(r'^makeRestore/',views.makeRestore),
    url(r'^sendMessage/',views.sendMessage),
    url(r'^deleteMessage/',views.deleteMessage),
    url(r'^',views.main),

)