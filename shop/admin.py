from django.contrib import admin
from .models import Item, Discount, Tax, Order

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'currency')  # Display fields in list view
    search_fields = ('name', 'description')  # Enable search functionality

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name', 'persentage')  # Display fields in list view
    search_fields = ('name',)  # Enable search functionality

@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('name', 'persentage')  # Display fields in list view
    search_fields = ('name',)  # Enable search functionality

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'get_total_price')  # Display fields in list view
    search_fields = ('created_at',)  # Enable search functionality
    filter_horizontal = ('items',)  # Use a filter for ManyToMany fields

    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = 'Total Price'
