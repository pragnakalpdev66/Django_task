from django.db import models # type: ignore
from django.core.validators import MaxValueValidator, MinValueValidator # type: ignore

class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

class Person(models.Model):
    class Role(models.TextChoices):
        # (“actor”, “Actor”), (“director”, “Director”), (“writer”, “Writer”)
        ACTOR = 'actor', 'Actor'
        DIRECTOR = 'director', 'Director'
        WRITER = 'writer', 'Writer'

    name = models.CharField(max_length=100)
    role_type = models.CharField(max_length=10, choices=Role.choices)
    bio = models.TextField
    birth_date = models.DateField

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField
    release_year = models.PositiveIntegerField
    duration = models.PositiveIntegerField(min)
    poster = models.ImageField(upload_to='posters/')
    rating = models.FloatField(default=0.0)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    director = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, limit_choices_to={'role_type': 'director'})
    created_at = models.DateTimeField(auto_now_add=True)

class MovieCast(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, limit_choices_to={'role_type': 'actor'})
    character_name = models.CharField(max_length=100)

class Language(models.Model):
    name = models.CharField(max_length=50, unique=True)

class MovieLanguage(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, message='rating must be at least 1'), 
            MaxValueValidator(10, message='rating cannot exceed 10')
        ]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)