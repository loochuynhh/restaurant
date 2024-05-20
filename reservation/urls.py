from django.urls import path
from . import views


urlpatterns = [
    path('find-tables/', views.view_available_tables, name='find-tables'),
    path('booking/', views.booking, name='booking'),
    path('booking/payment/<reservation_id>', views.payment, name='payment'),
    path('booking/payment_return', views.payment_return, name='payment_return'),
    # path('login/', views.login, name='login'),
    # path('logout/', views.logout, name='logout'),
    # path('forgotPassword/', views.forgotPassword, name='forgotPassword'),

    # path('dashboard/', views.dashboard, name='dashboard'),
    # path('', views.dashboard, name='dashboard'),

    # path('activate/<uidb64>/<token>', views.activate, name='activate'),
    # path('reset_password_validate/<uidb64>/<token>', views.reset_password_validate, name='reset_password_validate'),
    # path('reset_password/', views.reset_password, name='reset_password')
]
