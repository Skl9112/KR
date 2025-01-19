"""
URL configuration for HotelManagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from builder import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.auth, name='auth'),
    path('index/', views.index, name='index'),
    path('indexguest/', views.indexguest, name='indexguest'),
    path('rooms/', views.rooms, name='rooms'),
    path('roomsguest/', views.roomsguest, name='roomsguest'),
    path('client_reservations/', views.client_reservations, name='client_reservations'),
    path('make_payment/<int:reservation_id>/', views.make_payment, name='make_payment'),
    path('about/', views.about, name='about'),  # Новый маршрут
    path('booking/', views.booking, name='booking'),
    path('go_booking/', views.go_booking, name='go_booking'),
    path('login/', views.login, name='login'),  # Добавляем путь для входа
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

