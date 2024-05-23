from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from reservation.models import Reservation
from reservation.models import Payment
from django.views.decorators.csrf import csrf_exempt
from table.models import Table
from django.db.models import Q
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.conf import settings
from reservation.vnpay import vnpay
from reservation.form import PaymentForm
from order.models import Order
from menu.models import Menu
from django.utils.timezone import make_aware
# Create your views here.
DURATION = 2
HOUR_EXPIRED = 1
date_format = '%m/%d/%Y %I:%M %p'

@login_required(login_url="login")
@csrf_exempt
def get_reservation(request):
    user_id = request.user.id
    now = timezone.now()
    view = request.GET.get('view', 'all')

    if view == 'not_done':
        reservations = Reservation.objects.filter(user_id=user_id).exclude(end_time__lt=now).select_related('table')
    else:
        reservations = Reservation.objects.filter(user_id=user_id).select_related('table')

    reservations_with_table_name = []
    for reservation in reservations:
        reservation_with_table_name = {
            'start_time': reservation.start_time,
            'end_time': reservation.end_time,
            'people_count': reservation.people_count,
            'table_name': reservation.table.name,
            'total_price': reservation.total_price,
            'is_activated': reservation.is_activated
        }
        reservations_with_table_name.append(reservation_with_table_name)

    context = {
        'reservations': reservations_with_table_name,
        'now': now,
        'current_view': view,
    }
    return render(request, 'my_reservations.html', context)

        
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
    
    
    
@login_required(login_url="login")
@csrf_exempt
def payment(request):
    order_data = request.session.get('order_data', {})
    
    if not order_data:
        # Handle case where order_data is not in session
        return render(request, 'error.html', {"message": "No order data found in session"})
    
    start_time_str = order_data.get('start_time')
    end_time_str = order_data.get('end_time')
    total_price = order_data.get('total_money')

    date_format = '%m/%d/%Y %I:%M %p'
    start_time = make_aware(datetime.strptime(start_time_str, date_format))
    end_time = make_aware(datetime.strptime(end_time_str, date_format))

    # Check if reservation already exists
    reservation, created = Reservation.objects.get_or_create(
        start_time=start_time,
        end_time=end_time,
        people_count=order_data.get('people_count'),
        user_id=order_data.get('user_id'),
        table_id=order_data.get('id_table'),
        defaults={'total_price': total_price, 'is_activated': False}
    )
    
    if created:
        inputItem = order_data.get('inputItem', {})

        for item_name, details in inputItem.items():
            price = details['price']
            quantity = details['quantity']

            try:
                menu_item = Menu.objects.get(name=item_name)
                Order.objects.create(
                    menu=menu_item,
                    reservation=reservation,  
                    quantity=quantity
                )
            except Menu.DoesNotExist:
                print(f"Menu item '{item_name}' does not exist.")
                continue

    now = timezone.now()
    if reservation.creation_time > now + timedelta(hours=HOUR_EXPIRED):
        context = {
            "title": "Lỗi",
            "content": "Đơn đã quá giới hạn để thanh toán"
        }
        return render(request, 'content.html', context)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            order_type = "billpayment"
            order_id = form.cleaned_data['order_id']
            amount = form.cleaned_data['amount']
            order_desc = form.cleaned_data['order_desc']
            bank_code = form.cleaned_data['bank_code']
            language = form.cleaned_data['language']
            ipaddr = get_client_ip(request)

            # Check if payment already exists
            payment, payment_created = Payment.objects.get_or_create(
                order_id=order_id,
                defaults={
                    'order_type': order_type,
                    'amount': amount,
                    'order_desc': order_desc,
                    'bank_code': bank_code,
                    'language': language,
                    'reservation': reservation
                }
            )

            if payment_created:
                vnp = vnpay()
                vnp.requestData['vnp_Version'] = '2.1.0'
                vnp.requestData['vnp_Command'] = 'pay'
                vnp.requestData['vnp_TmnCode'] = settings.VNPAY_TMN_CODE
                vnp.requestData['vnp_Amount'] = amount * 100
                vnp.requestData['vnp_CurrCode'] = 'VND'
                vnp.requestData['vnp_TxnRef'] = order_id
                vnp.requestData['vnp_OrderInfo'] = order_desc
                vnp.requestData['vnp_OrderType'] = order_type
                vnp.requestData['vnp_CreateDate'] = datetime.now().strftime('%Y%m%d%H%M%S')
                vnp.requestData['vnp_IpAddr'] = ipaddr
                vnp.requestData['vnp_ReturnUrl'] = settings.VNPAY_RETURN_URL

                if language and language != '':
                    vnp.requestData['vnp_Locale'] = language
                else:
                    vnp.requestData['vnp_Locale'] = 'vn'
                
                if bank_code and bank_code != "":
                    vnp.requestData['vnp_BankCode'] = bank_code

                vnpay_payment_url = vnp.get_payment_url(settings.VNPAY_PAYMENT_URL, settings.VNPAY_HASH_SECRET_KEY)
                return redirect(vnpay_payment_url)
            else:
                print("Payment already exists")
                return redirect('error_page')
        else:
            print("Form input not valid")
    else:
        context = {
            "title": "Thanh toán",
            "reservation_id": reservation.id,
            "total_price": total_price
        }
        return render(request, "payment.html", context=context)



def payment_return(request):
    inputData = request.GET
    if inputData:
        vnp = vnpay()
        vnp.responseData = inputData.dict()
        order_id = inputData.get('vnp_TxnRef')
        amount = int(inputData.get('vnp_Amount')) / 100
        order_desc = inputData.get('vnp_OrderInfo')
        vnp_TransactionNo = inputData.get('vnp_TransactionNo')
        vnp_ResponseCode = inputData.get('vnp_ResponseCode')
        vnp_TmnCode = inputData.get('vnp_TmnCode')
        vnp_PayDate = inputData.get('vnp_PayDate')
        vnp_BankCode = inputData.get('vnp_BankCode')
        vnp_CardType = inputData.get('vnp_CardType')

        try:
            payment = Payment.objects.get(order_id=order_id)
        except Payment.DoesNotExist:
            # Handle case where payment does not exist
            return render(request, "payment_return.html", {"title": "Kết quả thanh toán", "result": "Lỗi", "msg": "Thanh toán không tồn tại."})

        reservation = payment.reservation

        if vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY):
            if vnp_ResponseCode == "00":
                if not reservation.is_activated:  # Only activate if not already activated
                    reservation.is_activated = True
                    reservation.save()
                
                payment.status = 'success'
                payment.save()

                current_site = get_current_site(request=request)
                mail_subject = 'Xác nhận thanh toán thành công'
                message = render_to_string('reservation_email.html', {
                    'user': reservation.user,
                    'table': reservation.table,
                    'reservation': reservation,
                    'ordered_menus': reservation.order_set.all()
                })
                send_email = EmailMessage(mail_subject, message, to=[reservation.user.email])
                send_email.content_subtype = 'html'  # Đặt kiểu nội dung thành HTML
                send_email.send()
                return render(request, "payment_return.html", {"title": "Kết quả thanh toán",
                                                               "result": "Thành công", "order_id": order_id,
                                                               "amount": amount, "order_desc": order_desc,
                                                               "vnp_TransactionNo": vnp_TransactionNo,
                                                               "vnp_ResponseCode": vnp_ResponseCode})
            else:
                payment.status = 'error'
                payment.save()
                return render(request, "payment_return.html", {"title": "Kết quả thanh toán",
                                                               "result": "Lỗi", "order_id": order_id,
                                                               "amount": amount, "order_desc": order_desc,
                                                               "vnp_TransactionNo": vnp_TransactionNo,
                                                               "vnp_ResponseCode": vnp_ResponseCode})
        else:
            return render(request, "payment_return.html",
                          {"title": "Kết quả thanh toán", "result": "Lỗi", "order_id": order_id, "amount": amount,
                           "order_desc": order_desc, "vnp_TransactionNo": vnp_TransactionNo,
                           "vnp_ResponseCode": vnp_ResponseCode, "msg": "Sai checksum"})
    else:
        return render(request, "payment_return.html", {"title": "Kết quả thanh toán", "result": ""})


        
def get_available_tables(start_time, end_time, people_count): 
    now = timezone.now()
    conflicting_reservations = Reservation.objects.filter(
        Q(start_time__lt=end_time) &
        Q(end_time__gt=start_time)
    ).exclude(
        creation_time__gt=now + timedelta(hours=1)
    ).values_list('table_id', flat=True)
    
    available_tables = Table.objects.exclude(id__in=conflicting_reservations).filter(capacity__gte=people_count)
    
    return available_tables

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip