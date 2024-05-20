from django.contrib import admin
from django.urls import include,path
from . import views
from django.conf.urls.static import static
from django.conf import settings 
urlpatterns = [
    path('', views.menu, name='menu'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)