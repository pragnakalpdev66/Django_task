from django.shortcuts import render, redirect # type: ignore
# from django.template import loader
from django.views import generic # type: ignore
# from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect # type: ignore

from movies.models import Genre
from movies.models import Person

# home
def HomePageView(request):
    return render(request, 'movies/home.html')

# movie
def MoviePageView(request):
    return render(request, 'movies/movie.html')

def AddMovieView(request):
    if request.method == 'POST':
        print("entering addmovie block")
    return render(request, 'movies/addmovie.html')

def MovieDetailView(request):
    return render(request, 'movies/movieDetail.html')

# people
def PeoplePageView(request):
    return render(request, 'movies/people.html')

@csrf_protect
def AddPeopleView(request):
    if request.method == 'POST':
        print("entering addpeople block")
        person_name = request.POST.get('person_name')
        role_type = request.POST.get('role_type')
        bio = request.POST.get('bio')
        if person_name:
            Person.objects.create(person_name=person_name)
            Person.objects.create(role_type=role_type)
            Person.objects.create(bio=bio)
            return redirect('movies:people')
    context = {
        'role_choices': Person.Role.choices,
    }
    return render(request, 'movies/addpeople.html')

# genre
def GenrePageView(request):
    print("GenrePageView called!")
    gneres = Genre.objects.all()
    return render(request, 'movies/genre.html',{"genres":gneres})

@csrf_protect
def AddGenreView(request):
    if request.method == 'POST':
        print("entering addgenre block")
        genre_name = request.POST.get('genre_name')
        if genre_name:  # Check: not empty
            Genre.objects.create(genre_name=genre_name)
            return redirect('movies:genre')

        # data = Genre(name = genre_name)
        # data = request.POST
        print("printingggggggg genreee:  ",genre_name)
        
        # return redirect('movies:addgenre') 
    return render(request, 'movies/addgenre.html')  ## if GET then render
    # data.save()

        # Genre.objects.create(
        #     genre_name = g_name
        # )
    return redirect('/GenrePageView')

