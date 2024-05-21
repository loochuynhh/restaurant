from django.shortcuts import render,redirect
from aboutUs.models import AboutUs
from menu.models import Menu
from comment.models import Comment
from comment.forms import CommentForm
from datetime import datetime
from django.contrib.auth import logout
def home(request):
    abouts = AboutUs.objects.all().order_by('type')
    for about in abouts:
        about.age = datetime.now().year - about.datetime.year
    foods = Menu.objects.filter(type=True)
    drinks = Menu.objects.filter(type=False)
    comments = Comment.objects.all().order_by('-created_at')
    form = CommentForm()
    context = {
        'foods': foods,
        'drinks': drinks,
        'abouts': abouts,
        'comments': comments, 
        'form': form
    }
    return render(request, 'index.html', context)
