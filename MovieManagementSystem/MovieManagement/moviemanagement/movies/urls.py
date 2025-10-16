from django.urls import path # type: ignore
from . import views

app_name = "movies"

urlpatterns = [
    path('homepage/', views.HomePageView, name='home'),
    path('moviepage/', views.MoviePageView, name='movie'),
    path('genrepage/', views.GenrePageView, name='genre'),
    path('peoplepage/', views.PeoplePageView, name='people'),
    path('addmoviepage/', views.AddMovieView, name='addmovie'),
    path('addgenrepage/', views.AddGenreView, name='addgenre'),
    path('addpeoplepage/', views.AddPeopleView, name='addpeople') 
]