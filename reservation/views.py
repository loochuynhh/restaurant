from django.shortcuts import render
from datetime import datetime, timedelta
from reservation.models import Reservation
from table.models import Table
from django.db.models import Q

# Create your views here.
DURATION = 2

def view_available_tables(request):
    if request.method == 'POST':
        start_time_str = request.POST.get('start_time')
        date_str = request.POST.get('date')
        people_count = int(request.POST.get('people_count', 0))

        start_time = datetime.fromisoformat(start_time_str)
        end_time = start_time + timedelta(hours=2)
        date = datetime.fromisoformat(date_str).date()

        available_tables = get_available_tables(start_time, end_time, date, people_count)

        context = {
            'available_tables': available_tables,
            'start_time': start_time,
            'end_time': end_time,
            'date': date,
            'people_count': people_count,
        }

        return render(request, 'booking.html', context)
    else:
        return render(request, 'booking.html')
        
def get_available_tables(start_time, end_time, date, people_count):
    conflicting_reservations = Reservation.objects.filter(
        Q(date=date) &
        Q(start_time__lt=end_time) &
        Q(end_time__gt=start_time)
    ).values_list('table_id', flat=True)
    
    available_tables = Table.objects.exclude(id__in=conflicting_reservations).filter(seats__gte=people_count)
    
    return available_tables