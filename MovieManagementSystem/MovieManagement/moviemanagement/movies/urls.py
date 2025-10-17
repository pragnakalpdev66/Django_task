from django.urls import path # type: ignore
from . import views

app_name = "movies"

urlpatterns = [
    path('homepage/', views.HomePageView, name='home'),

    path('moviepage/', views.MoviePageView, name='movie'),
    path('addmoviepage/', views.AddMovieView, name='addmovie'),
    path('movieDetailpage/', views.MovieDetailView, name='movieDetail'),
    
    path('genrepage/', views.GenrePageView, name='genre'),
    path('addgenrepage/', views.AddGenreView, name='addgenre'),
    
    path('peoplepage/', views.PeoplePageView, name='people'),
    path('addpeoplepage/', views.AddPeopleView, name='addpeople'),
]