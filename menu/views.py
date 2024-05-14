from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'menu.html')

# def about(request):
#     return render(request, 'app1/about.html')