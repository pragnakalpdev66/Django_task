from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.views import View # type: ignore
from django.views.generic import TemplateView, ListView # type: ignore
from django.views.decorators.csrf import csrf_protect # type: ignore
from django.utils.decorators import method_decorator # type: ignore
from movies.models import Genre, Person, Movie, MovieCast, Language, MovieLanguage

# Home
class HomePageView(TemplateView):
    template_name = 'movies/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        # filter on genre
        # context['movies'] = Movie.objects.all()
        selected_genre = self.request.GET.get('genre')
        if selected_genre:
            context['movies'] = Movie.objects.filter(genre__name=selected_genre)
        else:
            context['movies'] = Movie.objects.all()
        return context

# Movie
class MoviePageView(ListView):
    model = Movie
    template_name = 'movies/movie.html'
    context_object_name = 'movies'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        context['years'] = Movie.release_year

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        print("movie list printing..")

        genres_list = self.request.GET.getlist('genres')
        print(f"genre: {genres_list}") ## 
        years_list = self.request.GET.get('years_list')
        search_query = self.request.GET.get('search_movie')
        print(f"search_query: {search_query}") ## 

        if genres_list and 'all' not in genres_list:
            print("filter with genre block..")
            queryset = queryset.filter(genre__in=genres_list)
        if years_list and years_list != "all":
            print("filter with year block..")
            queryset = queryset.filter(years_list=years_list)
        if search_query:
            print("filter with search-query block..")
            queryset = queryset.filter(title__icontains=search_query)
        
        return queryset
        

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

    def get(self, request, movie_id, *args, **kwargs):
        movie = get_object_or_404(Movie, id=movie_id)
        cast = MovieCast.objects.filter(movie_name=movie)
        languages = MovieLanguage.objects.filter(movie_name=movie)
        reviews = movie.reviews.all()  # uses related_name in Review model
        context = {
            'movie': movie,
            'cast': cast,
            'languages': languages,
            'reviews': reviews,
        }
        return render(request, self.template_name, context)

#People #peoplepageview
class PersonListView(ListView):
    model = Person
    template_name = 'movies/people.html'
    context_object_name = 'people'

    def get_queryset(self):
        queryset = super().get_queryset()
        print(f"Initial queryset count: {queryset.count()}") ##

        role_type = self.request.GET.get('role_type')
        search_query = self.request.GET.get('search_person')

        print(f"role_type: {role_type}") ## 
        print(f"search_query: {search_query}") ##

        if role_type and role_type != "all":
            queryset = queryset.filter(role_type=role_type)
            print(f"Filtered by role_type. New count: {queryset.count()}") ##
        # else:
        #     queryset = Person.objects.all()
        #     print(f"Display all role type. count: {queryset.count()}") #3

        if search_query:
            queryset = queryset.filter(person_name__icontains=search_query)
            print(f"Filtered by search_query. New count: {queryset.count()}") ##

        print(f"Final queryset count: {queryset.count()}") ##

        return queryset#.order_by('person_name')

    # def get_context_data(self, **kwargs):
    #     # context = super().get_context_data(**kwargs)
    #     context = {'role_choices': Person.Role.choices}
    #     context['people'] = Person.objects.all() # & Person.Role.choices # have to add query
    #     return context
    
class PersonDetailView(TemplateView):
    template_name = 'movies/personDetail.html'
    
    def get(self, request, person_id, *args, **kwargs):
        person = get_object_or_404(Person, id=person_id)

        context = {'person':person}
        return render(request, self.template_name,context)

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
        birth_date = request.POST.get('birth_date')
        bio = request.POST.get('biography') or request.POST.get('bio')

        if person_name and role_type:
            Person.objects.create(person_name=person_name, role_type=role_type, birth_date=birth_date, bio=bio)
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
        languages = ['English', 'Spanish', 'French', 'Filipino'] # Language.objects.all() # MovieLanguage.objects.all()
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
            actor_id = request.POST.get('actor_id')
            character_name = request.POST.get('character_name')
            if actor_id and character_name:
                actor = Person.objects.filter(id=actor_id, role_type=Person.Role.ACTOR).first()
                if actor:
                    MovieCast.objects.create(movie_name=movie, person=actor, character_name=character_name)


        elif 'add_language' in request.POST:
            lang_value = request.POST.get('language')
            if lang_value:
                lang_obj = None
                try:
                    if str(lang_value).isdigit():
                        lang_obj = Language.objects.filter(id=int(lang_value)).first()
                except Exception:
                    lang_obj = None

                if not lang_obj:
                    lang_obj, _ = Language.objects.get_or_create(language=lang_value)

                if lang_obj:                   
                    MovieLanguage.objects.create(movie_name=movie, language=lang_obj)

        elif 'done' in request.POST:
            return redirect('movies:moviedetail',movie_id=movie.id)

        return redirect('movies:manage_cast_language', movie_id=movie.id)
