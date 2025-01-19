from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, RoomCategory, Client, Reservation, News, FAQ, Review
from .models import Payment
from django.utils import timezone
from django.db.models import F

from builder.models import News

def index(request):
    news_items = News.objects.all().order_by('-created_at')
    faqs = FAQ.objects.all().order_by('-created_at')
    reviews = Review.objects.annotate(rating_range=F('rating')).order_by('-created_at')  # Передаём rating в контекст
    return render(request, 'index.html', {
        'news_items': news_items,
        'faqs': faqs,
        'reviews': reviews,
    })

def indexguest(request):
    return render(request, 'indexguest.html')

def rooms(request):
    rooms = Room.objects.all()  # Получаем все объекты номеров из базы данных
    categories = RoomCategory.objects.all()  # Получаем все категории номеров из базы данных

    # Получаем значение параметра category из запроса GET
    category = request.GET.get('category')

    return render(request, 'room.html', {'rooms': rooms, 'categories': categories, 'category': category})

def roomsguest(request):
    rooms = Room.objects.all()  # Получаем все объекты номеров из базы данных
    categories = RoomCategory.objects.all()  # Получаем все категории номеров из базы данных

    # Получаем значение параметра category из запроса GET
    category = request.GET.get('category')

    return render(request, 'roomguest.html', {'rooms': rooms, 'categories': categories, 'category': category})


def auth(request):
    return render(request, 'Auth.html')

def admin(request):
    return render(reqest, 'admin')

def login(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        if user_type == 'client':
            try:
                client = Client.objects.get(first_name=name, phone=phone)
                # Если клиент найден, перенаправляем на страницу index.html
                return render(request, 'index.html')
            except Client.DoesNotExist:
                # Если клиент не найден, остаемся на странице входа с сообщением об ошибке
                return render(request, 'auth.html', {'error_message': 'Неверное имя, номер телефона или пароль'})
        if user_type == 'admin':
            # Если пользователь является администратором, перенаправляем его на страницу администратора
            return redirect('admin:index')

    else:
        return render(request, 'auth.html')

def about(request):
    return render(request, 'about.html')  # Укажите путь к вашему шаблону

def go_booking(request):
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        if room_id:
            try:
                room = Room.objects.get(pk=room_id)
                return render(request, 'booking.html', {'room': room})
            except Room.DoesNotExist:
                return HttpResponse('Room not found', status=404)
        else:
            return redirect('rooms')  # Перенаправляем пользователя на страницу с доступными номерами
    else:
        return HttpResponse('Method not allowed', status=405)

from datetime import datetime

def booking(request):
    if request.method == 'POST':
        room = request.POST.get('room_id')
        client_first_name = request.POST.get('client_first_name')
        client_last_name = request.POST.get('client_last_name')
        check_in_date = datetime.strptime(request.POST.get('check_in_date'), '%Y-%m-%d')
        check_out_date = datetime.strptime(request.POST.get('check_out_date'), '%Y-%m-%d')

        try:
            client = Client.objects.get(first_name=client_first_name, last_name=client_last_name)
        except Client.DoesNotExist:
            return HttpResponse('Клиент не найден', status=404)

        try:
            room2 = Room.objects.get(room_id=room)
        except Room.DoesNotExist:
            return HttpResponse('Номер не найден', status=404)

        # Рассчитываем количество дней пребывания
        days_stayed = (check_out_date - check_in_date).days

        # Проверяем, что дата выезда позже даты заезда
        if days_stayed <= 0:
            return HttpResponse('Дата выезда должна быть позже даты заезда', status=400)

        # Рассчитываем общую стоимость
        total_price = days_stayed * room2.price

        reservation = Reservation.objects.create(
            room_id=room,
            client_id=client.client_id,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            total_price=total_price
        )

        return render(request, 'index.html')
    else:
        return HttpResponse('Method not allowed', status=405)

def client_reservations(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        try:
            client = Client.objects.get(phone=phone_number)
            reservations = Reservation.objects.filter(client=client)
            return render(request, 'client_reservations.html', {'client': client, 'reservations': reservations})
        except Client.DoesNotExist:
            error_message = 'Клиент с таким номером телефона не найден.'
            return render(request, 'client_reservations.html', {'error_message': error_message})
    return render(request, 'client_reservations.html')

def make_payment(request, reservation_id):
    if request.method == 'POST':
        reservation = Reservation.objects.get(reservation_id=reservation_id)
        amount = request.POST.get('amount')
        payment = Payment(reservation=reservation, amount=amount, payment_date=timezone.now(), status='paid')
        payment.save()
        return redirect('client_reservations')
    return redirect('client_reservations')  # или другая страница, если что-то пошло не так