from django.shortcuts import render # type: ignore
from django.template import loader

from django.views import generic # type: ignore

# class HomePageView(TemplateView):
#     template_name = 'movies/home.html'

from django.http import HttpResponse

# class HomePageView(generic):

# def get(self, request, *args, **kwargs):
#     template = loader.get_template('home.html')
#     return HttpResponse(template.render())

#     #     return HttpResponse("Hello world!")

def HomePageView(request):
    return render(request, 'movies/home.html')

def MoviePageView(request):
    return render(request, 'movies/movie.html')

def GenrePageView(request):
    return render(request, 'movies/genre.html')

def PeoplePageView(request):
    return render(request, 'movies/people.html')

def AddMovieView(request):
    return render(request, 'movies/addmovie.html')

def AddGenreView(request):
    return render(request, 'movies/addgenre.html')

def AddPeopleView(request):
    return render(request, 'movies/addpeople.html')
