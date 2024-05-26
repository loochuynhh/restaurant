from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from .models import Order
from .models import Menu
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
DURATION = 2
HOUR_EXPIRED = 1
date_format = '%m/%d/%Y %I:%M %p'

@login_required(login_url="login")
@csrf_exempt
def order(request):
    if request.method == "POST":
        user_id = request.user.id
        id_table = request.POST.get('tableid')
        start_time_str = request.POST.get('starttime')
        people_count = int(request.POST.get('people_count', 0))
        foods = Menu.objects.filter(type=True)
        drinks = Menu.objects.filter(type=False)
        start_time = datetime.strptime(start_time_str, '%m/%d/%Y %I:%M %p')  # Sửa đổi ở đây
        end_time = start_time + timedelta(hours=DURATION)
        start_time_str = start_time.strftime('%m/%d/%Y %I:%M %p')
        end_time_str = end_time.strftime('%m/%d/%Y %I:%M %p')
        request.session['order_data'] = {
            'user_id': user_id,
            'id_table': id_table,
            'start_time': start_time_str,
            'end_time': end_time_str,
            'people_count': people_count,
        }
        context = {
                'user_id': user_id,
                'id_table': id_table,
                'foods': foods,
                'drinks': drinks,
                'start_time': start_time,
                'end_time': end_time,
                'people_count': people_count,
            }
        return render(request, 'order.html', context)
    else:
        return render(request, 'booking.html')

@login_required(login_url="login")
@csrf_exempt
def book_order(request):
    if request.method == "POST":
        order_data = request.session.get('order_data', {})
        start_time_str = order_data.get('start_time')
        end_time_str = order_data.get('end_time')
        people_count = order_data.get('people_count')
        user_id = order_data.get('user_id')
        id_table = order_data.get('id_table')
        total_money = request.POST.get('total_money')
        input_item_list = request.POST.get('inputItemList')
        item = json.loads(input_item_list)
        request.session['order_data'] = {
            'total_money': total_money,
            'user_id': user_id,
            'id_table': id_table,
            # 'foods': foods,
            'inputItem': item,
            'start_time': start_time_str,
            'end_time': end_time_str,
            'people_count': people_count,
        }
        return redirect('payment')
    else:
        user_id = request.user.id
        id_table = request.POST.get('tableid')
        start_time_str = request.POST.get('starttime')
        people_count = int(request.POST.get('people_count', 0))
        foods = Menu.objects.filter(type=True)
        drinks = Menu.objects.filter(type=False)
        start_time = datetime.strptime(start_time_str, date_format)
        end_time = start_time + timedelta(hours=DURATION)
        context = {
                'user_id': user_id,
                'id_table': id_table,
                'foods': foods,
                'drinks': drinks,
                'start_time': start_time,
                'end_time': end_time,
                'people_count': people_count,
            }
        return render(request, 'order.html', context)
