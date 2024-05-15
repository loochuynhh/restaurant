from django.shortcuts import render

# Create your views here.
def about(request):
    return render(request, 'about.html')

# def about(request):
#     return render(request, 'app1/about.html')