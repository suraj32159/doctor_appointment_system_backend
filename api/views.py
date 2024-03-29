import stripe
from django.conf import settings
from django.http import JsonResponse
from rest_framework import generics, mixins, status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.views import APIView

from google_services.services import generate_meet_link
from mailer.send_mail import SendMail
from .models import BookAppointment
from .serializers import BookAppointmentSerializer, UserSerializer


class BookAppointmentAPIView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView, SendMail):
    queryset = BookAppointment.objects.all()
    serializer_class = BookAppointmentSerializer

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User with specified ID does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        appointments = self.get_queryset().filter(user=user)
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User with specified ID does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data, context={'user_id': user.id})
        if serializer.is_valid():
            gmeet_link = ""
            # gmeet_link = generate_meet_link()
            serializer.validated_data['gmeet_link'] = gmeet_link
            serializer.save(user=user)
            try:
                # self.send_mail_to.apply_async(kwargs={"params": request.data, "gmeet_link": gmeet_link})
                self.send_mail_to(request.data, gmeet_link)
            except Exception as e:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCreateAPIView(CreateModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()


class CreateCheckoutSession(APIView):
    def get(self, request):
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items
                =[{
                    'price_data': {
                        'currency': 'inr',
                        'unit_amount': 500,
                        'product_data': {
                            'name': 'T-shirt',
                            'description': 'Comfortable cotton t-shirt',
                            'images': ['https://example.com/t-shirt.png'],
                        },
                    },
                    'quantity': 1,
                }]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})
