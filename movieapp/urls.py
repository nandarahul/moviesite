from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'movies/search/?$', views.search_movie),
    url(r'movies/toprated/?$', views.get_top_rated),
    url(r'movie/?$', views.add_movie),
    url(r'actor/?$', views.add_actor),
    url(r'director/?$', views.add_director),
    url(r'genre/?$', views.add_genre),

]