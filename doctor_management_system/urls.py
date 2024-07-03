from django.contrib import admin
from django.urls import path, include
from api.views import BookAppointmentAPIView, UserCreateAPIView, CreateCheckoutSession

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/appointment/', BookAppointmentAPIView.as_view(), name='book_appointment'),
    path('api/appointment/<str:email>/', BookAppointmentAPIView.as_view(), name='book_appointment_by_email'),
    path('api/user/', UserCreateAPIView.as_view(), name='user-create'),
    path('create-checkout-session/', CreateCheckoutSession.as_view(), name='create_checkout_session'),
    # path('payments/', include('payments.urls'))
]
