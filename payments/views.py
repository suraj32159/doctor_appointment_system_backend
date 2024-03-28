import stripe
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

stripe.api_key = "your_stripe_api_key"


@api_view(['POST'])
def test_payment(request):
    test_payment_intent = stripe.PaymentIntent.create(
        amount=1000,
        currency='pln',
        payment_method_types=['card'],
        receipt_email='test@example.com'
    )
    return Response(status=status.HTTP_200_OK, data=test_payment_intent)
