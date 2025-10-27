from django.urls import path # type: ignore
from . import views

app_name = "movies"

urlpatterns = [
    path('homepage/', views.HomePageView.as_view(), name='home'),

    path('moviepage/', views.MoviePageView.as_view(), name='movie'),
    path('addmoviepage/', views.AddMovieView.as_view(), name='addmovie'),
    path('movie/manage_cast_language/<int:movie_id>/', views.ManageCastLanguagesView.as_view(), name='manage_cast_language'),
    path('movieDetailpage/', views.MovieDetailView.as_view(), name='movieDetail'),
    
    path('genrepage/', views.GenrePageView.as_view(), name='genre'),
    path('addgenrepage/', views.AddGenreView.as_view(), name='addgenre'),
    
    path('peoplepage/', views.PeoplePageView.as_view(), name='people'),
    path('addpeoplepage/', views.AddPeopleView.as_view(), name='addpeople'),
    path('personDetailpage/', views.PersonDetailView.as_view(), name='personDetail'),
]