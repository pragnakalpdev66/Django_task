from django.urls import path
from . import views

urlpatterns = [
    path("about/", views.MyView.as_view()),
    path("greeting/", views.GreetingsView.as_view(greetings="good-day!")),
    path("greetings/", views.MorningGreetingView.as_view())
]