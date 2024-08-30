import stripe
from django.conf import settings
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Item

stripe.api_key = settings.STRIPE_SECRET_KEY

@api_view(['GET'])
def buy_item(request, id):
    """Get Stripe Session ID for a selected item."""
    item = get_object_or_404(Item, id=id)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': item.currency,
                'product_data': {
                    'name': item.name,
                },
                'unit_amount': int(item.price * 100),  # converting to cents
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri('/success/'),
        cancel_url=request.build_absolute_uri('/cancel/'),
    )
    return Response({'sessionId': session.id})


@api_view(['GET'])
def item_detail(request, id):
    """Get HTML page with item details and a Buy button."""
    try:
        item = Item.objects.get(id=id)
    except Item.DoesNotExist:
        raise Http404("Item not found")

    return render(request, 'item_detail.html', {'item': item, 'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY})
