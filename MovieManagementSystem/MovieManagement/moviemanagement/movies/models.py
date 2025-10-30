from django.db import models # type: ignore
from django.core.validators import MaxValueValidator, MinValueValidator # type: ignore

class Genre(models.Model):
    genre_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.genre_name

class Person(models.Model):
    class Role(models.TextChoices):
        # (“actor”, “Actor”), (“director”, “Director”), (“writer”, “Writer”)
        ACTOR = 'actor', 'Actor'
        DIRECTOR = 'director', 'Director'
        WRITER = 'writer', 'Writer'

    person_name = models.CharField(max_length=100)
    role_type = models.CharField(max_length=10, choices=Role.choices)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.person_name

    birth_date = models.DateField(null=True, blank=True)

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(default=None)
    release_year = models.PositiveIntegerField(null=True)
    duration = models.PositiveIntegerField()
    poster = models.ImageField(upload_to='posters/', null=True, blank=True)
    rating = models.FloatField(default=0.0)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    director = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, limit_choices_to={'role_type': 'director'})
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.release_year})"


class MovieCast(models.Model):
    movie_name = models.ForeignKey(Movie, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, limit_choices_to={'role_type': 'actor'})
    character_name = models.CharField(max_length=100)

    class Meta:
        unique_together = (('movie_name', 'person'),)


class Language(models.Model):
    language = models.CharField(max_length=50, unique=True)
    # languages = ['English', 'Spanish', 'French', 'Filipino']

    def __str__(self):
        return self.language

class MovieLanguage(models.Model):
    movie_name = models.ForeignKey(Movie, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.language}"

    class Meta:
        unique_together = (('movie_name', 'language'),)

class Review(models.Model):
    movie_name = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user_name = models.ForeignKey(Person, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, message='rating must be at least 1'), 
            MaxValueValidator(10, message='rating cannot exceed 10')
        ]
    )
    comment = models.TextField(default=None)
    created_at = models.DateTimeField(auto_now_add=True)