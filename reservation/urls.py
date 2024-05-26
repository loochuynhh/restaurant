from django.urls import path
from . import views


urlpatterns = [
    path('find-tables/', views.view_available_tables, name='find-tables'),
<<<<<<< HEAD
    path('booking/', views.booking, name='booking'),
    path('booking/payment/<reservation_id>', views.payment, name='payment'),
=======
    path('booking/payment/', views.payment, name='payment'),
>>>>>>> Restaurant/master
    path('booking/payment_return', views.payment_return, name='payment_return'),
    path('my_reservations/', views.get_reservation, name='my_reservations'),
]
