from django.urls import path
from . import views


urlpatterns = [
    path('find-tables/', views.view_available_tables, name='find-tables'),
    path('booking/payment/', views.payment, name='payment'),
    path('booking/payment_return', views.payment_return, name='payment_return'),
    path('my_reservations/', views.get_reservation, name='my_reservations'),
]
