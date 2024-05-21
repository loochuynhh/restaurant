from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from reservation.models import Reservation
from reservation.models import Payment
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
from django.conf import settings

from reservation.vnpay import vnpay
from reservation.form import PaymentForm

# Create your views here.
DURATION = 2
HOUR_EXPIRED = 1
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

        
        reservation = Reservation.objects.create(
            start_time=start_time,
            end_time=end_time,
            people_count=people_count,
            user_id = user_id,
            table_id=id_table,
            is_activated = False
        )
        return redirect('payment/' + str(reservation.id))
        
    else:
        return render(request, 'get_empty_tables.html')
        
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
    
def payment(request, reservation_id):
    reservation = Reservation.objects.get(pk=reservation_id)

    now = timezone.now()

    if reservation.creation_time > now + timedelta(hours=HOUR_EXPIRED):
        context =  {
            "title": "Lỗi",
            "content" : "Đơn đã quá giới hạn để thanh toán"
        }
        return render(request, 'content.html', context)
    if request.method == 'POST':
        # Process input data and build url payment
        form = PaymentForm(request.POST)
        if form.is_valid():
            order_type = "billpayment"
            order_id = form.cleaned_data['order_id']
            amount = form.cleaned_data['amount']
            order_desc = form.cleaned_data['order_desc']
            bank_code = form.cleaned_data['bank_code']
            language = form.cleaned_data['language']
            ipaddr = get_client_ip(request)
            
            payment = Payment.objects.create(
                order_id=order_id,
                order_type=order_type,
                amount=amount,
                order_desc = order_desc,
                bank_code=bank_code,
                language=language,
                reservation_id=reservation_id
            )
            
            # Build URL Payment
            vnp = vnpay()
            vnp.requestData['vnp_Version'] = '2.1.0'
            vnp.requestData['vnp_Command'] = 'pay'
            vnp.requestData['vnp_TmnCode'] = settings.VNPAY_TMN_CODE
            vnp.requestData['vnp_Amount'] = amount * 100
            vnp.requestData['vnp_CurrCode'] = 'VND'
            vnp.requestData['vnp_TxnRef'] = order_id
            vnp.requestData['vnp_OrderInfo'] = order_desc
            vnp.requestData['vnp_OrderType'] = order_type
            # Check language, default: vn
            if language and language != '':
                vnp.requestData['vnp_Locale'] = language
            else:
                vnp.requestData['vnp_Locale'] = 'vn'
                # Check bank_code, if bank_code is empty, customer will be selected bank on VNPAY
            if bank_code and bank_code != "":
                vnp.requestData['vnp_BankCode'] = bank_code

            vnp.requestData['vnp_CreateDate'] = datetime.now().strftime('%Y%m%d%H%M%S')  # 20150410063022
            vnp.requestData['vnp_IpAddr'] = ipaddr
            vnp.requestData['vnp_ReturnUrl'] = settings.VNPAY_RETURN_URL
            vnpay_payment_url = vnp.get_payment_url(settings.VNPAY_PAYMENT_URL, settings.VNPAY_HASH_SECRET_KEY)
            print(vnpay_payment_url)
            return redirect(vnpay_payment_url)
        else:
            print("Form input not validate")
    else:
        context =  {
            "title": "Thanh toán",
            "reservation_id" : reservation_id
        }
        return render(request, "payment.html", context=context)
    
def payment_return(request):
    inputData = request.GET
    if inputData:
        vnp = vnpay()
        vnp.responseData = inputData.dict()
        order_id = inputData['vnp_TxnRef']
        amount = int(inputData['vnp_Amount']) / 100
        order_desc = inputData['vnp_OrderInfo']
        vnp_TransactionNo = inputData['vnp_TransactionNo']
        vnp_ResponseCode = inputData['vnp_ResponseCode']
        vnp_TmnCode = inputData['vnp_TmnCode']
        vnp_PayDate = inputData['vnp_PayDate']
        vnp_BankCode = inputData['vnp_BankCode']
        vnp_CardType = inputData['vnp_CardType']
        payment = Payment.objects.get(order_id=order_id)
        reservation = payment.reservation
        if vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY):
            if vnp_ResponseCode == "00":
                reservation.is_activated = True
                reservation.save()
                payment.status = 'success'
                payment.save()
                return render(request, "payment_return.html", {"title": "Kết quả thanh toán",
                                                               "result": "Thành công", "order_id": order_id,
                                                               "amount": amount,
                                                               "order_desc": order_desc,
                                                               "vnp_TransactionNo": vnp_TransactionNo,
                                                               "vnp_ResponseCode": vnp_ResponseCode})
            else:
                payment.status = 'error'
                payment.save()
                return render(request, "payment_return.html", {"title": "Kết quả thanh toán",
                                                               "result": "Lỗi", "order_id": order_id,
                                                               "amount": amount,
                                                               "order_desc": order_desc,
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