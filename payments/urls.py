from django.urls import path
from payments import views

urlpatterns = [
    path('test-payment/', views.test_payment, name='test_payment'),
]
