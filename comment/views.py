from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Comment
from .forms import CommentForm
# Create your views here.
# @login_required
@login_required(login_url="login")
def post_comment(request):
    if request.method == "POST":
        print('1')
        form = CommentForm(request.POST)
        if form.is_valid():
            print('2')
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return JsonResponse({
                    'status':'success',
                    'comment': comment.content,
                    'user': comment.user.username,
                    'created_at' : comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
                })
            # return redirect('forum')
        else:
            print('3')
            if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'errors': form.errors
                })
    print('4')
    comments = Comment.objects.all().order_by('-created_at')
    form = CommentForm()
    return render(request, 'forum.html', {'comments': comments, 'form': form})
def forum(request):
    comments = Comment.objects.all().order_by('-created_at')
    form = CommentForm()
    return render(request, 'forum.html', {'comments': comments, 'form': form})
