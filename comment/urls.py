from django.contrib import admin
from django.urls import include,path
from . import views
from django.conf.urls.static import static
from django.conf import settings 
urlpatterns = [
    path('', views.forum, name='forum'),
    path('post_comment/', views.post_comment, name='post_comment'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)