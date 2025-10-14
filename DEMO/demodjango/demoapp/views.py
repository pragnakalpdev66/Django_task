from django.shortcuts import render
# from django.http  import HttpResponse

# Create your views here.
def demo(request):
    # return HttpResponse("demo ptoject")
    return render(request ,'index.html', {'name':'patel'})

def home(request):
    return render(request, 'home.html')