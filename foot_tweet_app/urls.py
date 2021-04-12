from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'foot_tweet_app'
urlpatterns = [
    path(r'/foot_tweet_app/', views.index, name='index'),
    path(r'help/', views.help, name='help'),
    url(r'^show_team/$',views.show_team,name='show_team'),
    url(r'^show_player/$',views.show_player,name='show_player'),
]