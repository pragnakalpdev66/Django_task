from django.urls import path # type: ignore
from . import views

app_name = "movies"

urlpatterns = [
    path('homepage/', views.HomePageView.as_view(), name='home'),

    path('moviepage/', views.MoviePageView.as_view(), name='movie'),
    path('addmoviepage/', views.AddEditMovieView.as_view(), name='addmovie'),
    path('editmoviepage/<int:movie_id>/', views.AddEditMovieView.as_view(), name='editmovie'), ##
    path('deletemovie/<int:pk>/', views.DeleteMovie.as_view(), name='deletemovie'),
    path('movieDetailpage/<int:movie_id>/', views.MovieDetailView.as_view(), name='movieDetail'),

    path('movie/manage_cast_language/<int:movie_id>/', views.ManageCastLanguagesView.as_view(), name='manage_cast_language'),
    # path('removecast/<int:pk>/', views.RemoveCast.as_view(), name='removeCast'),
    # path('removecast/<int:pk>/', views.RemoveCast.as_view(), name='removeCast'),
    
    path('genrepage/', views.GenrePageView.as_view(), name='genre'),
    path('addgenrepage/', views.AddGenreView.as_view(), name='addgenre'),
    
    path('peoplepage/', views.PersonListView.as_view(), name='people'),
    path('addpeoplepage/', views.AddEditPeopleView.as_view(), name='addpeople'),
    path('editpeoplepage/<int:person_id>/', views.AddEditPeopleView.as_view(), name='editpeople'), ##
    path('deletepeople/<int:pk>/', views.DeletePeople.as_view(), name='deletepeople'),
    path('personDetailpage/<int:person_id>/', views.PersonDetailView.as_view(), name='personDetail'),
]