from django.db import models


class Hotel(models.Model):
    hotel_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'hotels'


class RoomCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'roomcategories'


class Room(models.Model):
    room_id = models.AutoField(primary_key=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    category = models.ForeignKey(RoomCategory, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=50)
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    AVAILABILITY_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
    ]
    availability = models.CharField(max_length=10, choices=AVAILABILITY_CHOICES, default='available')
    photo = models.ImageField(upload_to='images')  # Путь для загрузки фотографий

    class Meta:
        managed = False
        db_table = 'rooms'


class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50)
    has_child = models.BooleanField(default=False)
    comment = models.TextField()
    phone = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'clients'


class Reservation(models.Model):
    reservation_id = models.AutoField(primary_key=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'reservations'


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unpaid')

    class Meta:
        managed = False
        db_table = 'payments'


class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='news_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'builder_news'

class FAQ(models.Model):
    question = models.CharField(max_length=500)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'builder_faq'

    def __str__(self):
        return self.question

class Review(models.Model):
    client_name = models.CharField(max_length=100)  # Имя клиента
    client_photo = models.ImageField(upload_to='client_photos/', null=True, blank=True)  # Фото клиента
    review_text = models.TextField()  # Текст отзыва
    rating = models.PositiveIntegerField(default=1, choices=[(i, f'{i} звезд') for i in range(1, 6)])  # Рейтинг (1-5 звёзд)
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания

    class Meta:
        db_table = 'builder_review'

    def __str__(self):
        return f'{self.client_name} - {self.rating} звезд'
