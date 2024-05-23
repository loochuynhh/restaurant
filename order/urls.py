from django.contrib import admin
from django.urls import include,path
from . import views
from django.conf.urls.static import static
from django.conf import settings 
urlpatterns = [
    path('', views.order, name='order'),
    path('book_order', views.book_order, name='book_order'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)