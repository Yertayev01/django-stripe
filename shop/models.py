from django.db import models
from decimal import Decimal  # Импортируем Decimal для правильного приведения типов

class Item(models.Model):
    CURRENCY_CHOICES = [
        ('usd', 'USD'),
        ('eur', 'EUR'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='usd')

    def __str__(self):
        return self.name

class Discount(models.Model):
    name = models.CharField(max_length=255)
    persentage = models.FloatField()

    def __str__(self):
        return f"{self.name} ({self.persentage}%)"

class Tax(models.Model):
    name = models.CharField(max_length=255)
    persentage = models.FloatField()

    def __str__(self):
        return f"{self.name} ({self.persentage}%)"

class Order(models.Model):
    items = models.ManyToManyField(Item)
    discount = models.ForeignKey(Discount, null=True, blank=True, on_delete=models.SET_NULL)
    tax = models.ForeignKey(Tax, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total_price(self):
        total = sum(item.price for item in self.items.all())
        
        # Приведение типов и расчет скидок и налогов
        if self.discount:
            total -= total * Decimal(self.discount.persentage / 100)
        if self.tax:
            total += total * Decimal(self.tax.persentage / 100)

        return total
