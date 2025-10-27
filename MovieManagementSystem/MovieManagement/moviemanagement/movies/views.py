from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from movies.models import Genre, Person, Movie, MovieCast, MovieLanguage

# Home
class HomePageView(TemplateView):
    template_name = 'movies/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        # filter on genre
        return context

# Movie
class MoviePageView(TemplateView):
    template_name = 'movies/movie.html'

@method_decorator(csrf_protect, name='dispatch')
class AddMovieView(View):
    template_name = 'movies/addmovie.html'

    def get(self, request, *args, **kwargs):
        genres = Genre.objects.all()
        directors = Person.objects.filter(role_type=Person.Role.DIRECTOR)
        context = {'genres': genres, 'directors': directors}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        print("Entering AddMovieView POST block")

        title = request.POST.get('title')
        description = request.POST.get('description')
        release_year = request.POST.get('release_year')
        duration = request.POST.get('duration')
        genre_name = request.POST.get('genre') or request.POST.get('genre_name')
        director_id = request.POST.get('director')

        if title:
            genre_obj = None
            if genre_name:
                try:
                    if genre_name.isdigit():
                        genre_obj = Genre.objects.filter(id=int(genre_name)).first()
                    else:
                        genre_obj = Genre.objects.filter(genre_name__iexact=genre_name).first()
                except Exception as e:
                    print("Genre lookup error:", e)

            director_obj = None
            if director_id:
                try:
                    if director_id.isdigit():
                        director_obj = Person.objects.filter(
                            id=int(director_id),
                            role_type=Person.Role.DIRECTOR
                        ).first()
                except Exception as e:
                    print("Director lookup error:", e)

            try:
                movie = Movie.objects.create(
                    title=title,
                    description=description or None,
                    release_year=int(release_year) if release_year and release_year.isdigit() else None,
                    duration=int(duration) if duration and duration.isdigit() else None,
                    genre=genre_obj,
                    director=director_obj
                )
                print(f"Created movie: {movie}")
                # redirect to manage cast/language after adding
                return redirect('movies:manage_cast_language', movie_id=movie.id)
            except Exception as e:
                print("Error creating movie:", e)

        genres = Genre.objects.all()
        directors = Person.objects.filter(role_type=Person.Role.DIRECTOR)
        context = {'genres': genres, 'directors': directors}
        return render(request, self.template_name, context)

class MovieDetailView(TemplateView):
    template_name = 'movies/movieDetail.html'

#People
class PeoplePageView(TemplateView):
    template_name = 'movies/people.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context2 = {'role_choices': Person.Role.choices}
        context['people'] = Person.objects.all() # & Person.Role.choices # have to add query
        return context

    
class PersonDetailView(TemplateView):
    template_name = 'movies/personDetail.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

@method_decorator(csrf_protect, name='dispatch')
class AddPeopleView(View):
    template_name = 'movies/addpeople.html'

    def get(self, request, *args, **kwargs):
        context = {'role_choices': Person.Role.choices}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        print("Entering AddPeopleView POST block")
        person_name = request.POST.get('person_name')
        role_type = request.POST.get('role_type')
        bio = request.POST.get('biography') or request.POST.get('bio')

        if person_name and role_type:
            Person.objects.create(person_name=person_name, role_type=role_type, bio=bio)
            return redirect('movies:people')

        context = {'role_choices': Person.Role.choices}
        return render(request, self.template_name, context)

# Genre
class GenrePageView(TemplateView):
    template_name = 'movies/genre.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        return context

@method_decorator(csrf_protect, name='dispatch')
class AddGenreView(View):
    template_name = 'movies/addgenre.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        print("Entering AddGenreView POST block")
        genre_name = request.POST.get('genre_name')
        if genre_name:
            Genre.objects.create(genre_name=genre_name)
            return redirect('movies:genre')
        return render(request, self.template_name)


#cast and lang
@method_decorator(csrf_protect, name='dispatch')
class ManageCastLanguagesView(View):
    template_name = 'movies/manage_cast_language.html'

    def get(self, request, movie_id, *args, **kwargs):
        movie = get_object_or_404(Movie, id=movie_id)
        actors = Person.objects.filter(role_type=Person.Role.ACTOR)
        languages = MovieLanguage.objects.all()
        cast_list = MovieCast.objects.filter(movie_name=movie)
        movie_languages = MovieLanguage.objects.filter(movie_name=movie)

        context = {
            'movie': movie,
            'actors': actors,
            'languages': languages,
            'cast_list': cast_list,
            'movie_languages': movie_languages,
        }
        return render(request, self.template_name, context)

    def post(self, request, movie_id, *args, **kwargs):
        movie = get_object_or_404(Movie, id=movie_id)
        print("ManageCastLanguagesView POST triggered")

        if 'add_cast' in request.POST:
            actor_id = request.POST.get('actor')
            character_name = request.POST.get('character_name')
            if actor_id and character_name:
                actor = Person.objects.filter(id=actor_id, role_type=Person.Role.ACTOR).first()
                if actor:
                    MovieCast.objects.create(movie_name=movie, actor=actor, character_name=character_name)

        elif 'add_language' in request.POST:
            lang_code = request.POST.get('language')
            if lang_code:
                MovieLanguage.objects.create(movie_name=movie, language=lang_code)

        elif 'done' in request.POST:
            return redirect('movies:moviedetail')

        return redirect('movies:manage_cast_language', movie_id=movie.id)
