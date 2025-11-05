from django.contrib import admin

from .models import Genre, Person, Movie, MovieCast, Language, MovieLanguage, Review

admin.site.register(Genre)
admin.site.register(Person)
admin.site.register(Movie)
admin.site.register(MovieCast)
admin.site.register(Language)
admin.site.register(MovieLanguage)
admin.site.register(Review)
