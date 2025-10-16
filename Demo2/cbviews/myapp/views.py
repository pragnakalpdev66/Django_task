from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

class MyView(View):
    def get(self, request):
        return HttpResponse('result')
    
class GreetingsView(View):
    greetings = "Good Morning"

    def get(self, request):
        return HttpResponse(self.greetings)
    
# overriding greetings var but for display should have to use this class_name
class MorningGreetingView(GreetingsView):
    greetings = "Morning to ya"