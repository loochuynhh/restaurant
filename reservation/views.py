from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from reservation.models import Reservation
from django.views.decorators.csrf import csrf_exempt
from table.models import Table
from django.db.models import Q
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages, auth
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
DURATION = 2
HOUR_EXPIRED = 2
date_format = '%m/%d/%Y %I:%M %p'

@login_required(login_url="login")
@csrf_exempt
def booking(request):
    if request.method == "POST":
        user_id = request.user.id
        id_table = request.POST.get('tableid')
        start_time_str = request.POST.get('starttime')
        people_count = int(request.POST.get('people_count', 0))
        print(start_time_str)
        start_time = datetime.strptime(start_time_str, date_format)
        end_time = start_time + timedelta(hours=DURATION)
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        
        reservation = Reservation.objects.create(
            start_time=start_time,
            end_time=end_time,
            people_count=people_count,
            user_id = user_id,
            table_id=id_table
        )
        
        context = {
            'title': 'Đặt thành công',
            'content': 'Xin cảm ơn!'
        }
        return render(request, 'content.html', context)
    else:
        return render(request, 'find-tables.html')
        
@csrf_exempt
def view_available_tables(request):
    if request.method == "POST":
        start_time_str = request.POST.get('datetime')
        start_time_str = str(start_time_str)
        print(start_time_str)
        people_count = int(request.POST.get('people_count', 0))

        start_time = datetime.strptime(start_time_str, date_format)
        print(start_time)
        end_time = start_time + timedelta(hours=DURATION)

        available_tables = get_available_tables(start_time, end_time, people_count)

        context = {
            'available_tables': available_tables,
            'start_time': start_time_str,
            'end_time': end_time,
            'people_count': people_count,
        }
        print(start_time_str)

        return render(request, 'booking.html', context)
    else:
        return render(request, 'get_empty_tables.html')
        
def get_available_tables(start_time, end_time, people_count): 
    conflicting_reservations = Reservation.objects.filter(
        Q(start_time__lt=end_time) &
        Q(end_time__gt=start_time)
    ).values_list('table_id', flat=True)
    
    available_tables = Table.objects.exclude(id__in=conflicting_reservations).filter(capacity__gte=people_count)
    
    return available_tables