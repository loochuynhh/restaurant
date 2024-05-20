from django.shortcuts import render
from .models import Menu
# Create your views here.
def menu(request):
    foods = Menu.objects.filter(type=True)
    drinks = Menu.objects.filter(type=False)
    context = {
        'foods': foods,
        'drinks': drinks,
    }
    return render(request, 'menu.html', context)
