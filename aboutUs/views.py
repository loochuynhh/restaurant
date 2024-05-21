from django.shortcuts import render
from .models import AboutUs
from datetime import datetime
# Create your views here.
def about(request):
    abouts = AboutUs.objects.all().order_by('type')
    for about in abouts:
        about.age = datetime.now().year - about.datetime.year
    context = {
        'abouts': abouts,
    }
    return render(request, 'about.html', context)

