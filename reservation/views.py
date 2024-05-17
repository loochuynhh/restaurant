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

# Create your views here.
DURATION = 2
HOUR_EXPIRED = 2
date_format = '%m/%d/%Y %I:%M %p'

@csrf_exempt
def booking(request):
    if request.method == "POST":
        id_table = request.POST.get('tableid')
        start_time_str = request.POST.get('starttime')
        people_count = int(request.POST.get('people_count', 0))
        print(start_time_str)
        start_time = datetime.strptime(start_time_str, date_format)
        if request.POST.get('email') != None:
            
            end_time = start_time + timedelta(hours=DURATION)
            first_name = request.POST.get('firstname')
            last_name = request.POST.get('lastname')
            email = request.POST.get('email')
            message = request.POST.get('message')
            
            fullname = first_name + " " + last_name
            
            reservation = Reservation.objects.create(
                start_time=start_time,
                end_time=end_time,
                people_count=people_count,
                first_name=first_name,
                last_name=last_name,
                email=email,
                table_id=id_table
            )
            
            current_site = get_current_site(request=request)
            mail_subject = 'Activate your reservation.'
            message = render_to_string('active_email.html', {
                'fullname': fullname,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(reservation.id))
            })
            send_email = EmailMessage(mail_subject, message, to=[email])
            send_email.send()
            messages.success(
                request=request,
                message="Please confirm your email address to complete the registration"
            )
            
            context = {
                'title': 'Booking Successful',
                'content': 'Please check email to verify'
            }
            return render(request, 'content.html', context)
        else:
            context = {
                'tableid': id_table,
                'start_time': start_time_str,
                'people_count': people_count,
            }
            return render(request, 'booking.html', context)
        
def activate(request, uidb64):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        reservation = Reservation.objects.get(pk=uid)
    except Exception:
        reservation = None

    if reservation is not None:
        
        current_time = timezone.now()
        time_difference = current_time - reservation.creation_time
        if time_difference.total_seconds() > HOUR_EXPIRED * 3600:
            messages.error(request=request, message="Activation link has expired!")
            context = {
                'title': 'Activation has expired',
                'content': 'Your reservation has expired!'
            }
            return render(request, 'content.html', context)
        reservation.is_activated = True
        reservation.save()
        messages.success(
            request=request, message="Your revervation is activated!")
        context = {
            'title': 'Verify Successful',
            'content': 'Thanks for choosing us!'
        }
        return render(request, 'content.html', context)
    else:
        messages.error(request=request, message="Activation link is invalid!")
        return redirect('')

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

        return render(request, 'empty_tables.html', context)
    else:
        return render(request, 'get_empty_tables.html')
        
def get_available_tables(start_time, end_time, people_count):
    current_time = timezone.now()
    expiration_time = current_time - timedelta(HOUR_EXPIRED)
    
    conflicting_reservations = Reservation.objects.filter(
        Q(start_time__lt=end_time) &
        Q(end_time__gt=start_time) &
        ~Q(is_activated=False, creation_time__lt=expiration_time)
    ).values_list('table_id', flat=True)
    
    available_tables = Table.objects.exclude(id__in=conflicting_reservations).filter(capacity__gte=people_count)
    
    return available_tables