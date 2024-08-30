from django.core.management.base import BaseCommand
from shop.models import Item, Discount, Tax, Order
import random

class Command(BaseCommand):
    help = 'Populates the database with test data'

    def handle(self, *args, **kwargs):
        # Создаем тестовые товары
        items = [
            Item(name='Item 1', description='Description for item 1', price=100.00, currency='usd'),
            Item(name='Item 2', description='Description for item 2', price=150.50, currency='eur'),
            Item(name='Item 3', description='Description for item 3', price=200.99, currency='usd'),
        ]
        Item.objects.bulk_create(items)

        # Создаем тестовые скидки
        discounts = [
            Discount(name='Discount 1', persentage=10.0),
            Discount(name='Discount 2', persentage=15.0),
        ]
        Discount.objects.bulk_create(discounts)

        # Создаем тестовые налоги
        taxes = [
            Tax(name='Tax 1', persentage=5.0),
            Tax(name='Tax 2', persentage=8.0),
        ]
        Tax.objects.bulk_create(taxes)

        # Создаем заказы с случайными товарами, скидками и налогами
        for i in range(5):
            order = Order.objects.create(
                discount=random.choice(discounts),
                tax=random.choice(taxes)
            )
            order.items.set(random.sample(list(Item.objects.all()), k=2))  # Добавляем случайные товары к заказу
            order.save()

        self.stdout.write(self.style.SUCCESS('Database populated with test data successfully!'))
