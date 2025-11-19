from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin # type: ignore
from django.shortcuts import redirect, render # type: ignore
from django.contrib import messages # type: ignore
from movies.models import Genre, Person, Movie, MovieCast, Language, MovieLanguage, Review
from django.urls import resolve

class AdminRequiredMixin(UserPassesTestMixin):
    """Only allow admin role."""

    allowed_public_views = [
        'movies:home',
        'movies:movie',
        'movies:movieDetail',
        'movies:genre',
        'movies:people',
        'movies:personDetail',
    ]

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.user_role == 'admin'

    def handle_no_permission(self):
        messages.error(self.request, 'You do not have permission to access this page.')
        # return redirect('movies:home') 
        # movie_id = self.kwargs.get('movie_id')
        # person_id = self.kwargs.get('person_id')
        # if Movie:
        #     context = self.get_context_data(movie_id=movie_id)
        # elif Person:
        #     context = self.get_context_data(person_id_id=person_id)
          
          # return render(
        #     self.request, 
        #     'movies/home.html',
        #     # context
        # )

        current_view = resolve(self.request.path_info).view_name
        if current_view in self.allowed_public_views:
            return super().handle_no_per
        
        messages.error(self.request, 'You do not have permission to access this page.')
        return redirect('movies:home')
      

class UserAccessMixin(LoginRequiredMixin):
    """Allow only logged-in regular users to add reviews."""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.user_role == 'user'

    def handle_no_permission(self):
        return redirect('movies:signin')
