from django.contrib import admin
from .models import Hotel, RoomCategory, Room, Client, Reservation, Payment, News

admin.site.register(Hotel)
admin.site.register(RoomCategory)
admin.site.register(Room)
admin.site.register(Client)
admin.site.register(Reservation)
admin.site.register(Payment)
admin.site.register(News)

from .models import FAQ

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at')
    search_fields = ('question',)

    from .models import Review

    @admin.register(Review)
    class ReviewAdmin(admin.ModelAdmin):
        list_display = ('client_name', 'rating', 'created_at')
        search_fields = ('client_name', 'review_text')

