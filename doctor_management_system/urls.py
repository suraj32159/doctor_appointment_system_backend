from django.contrib import admin
from django.urls import path, include
from api.views import BookAppointmentAPIView, UserCreateAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/appointment/', BookAppointmentAPIView.as_view(), name='book_appointment'),
    path('api/appointment/<int:user_id>/', BookAppointmentAPIView.as_view(), name='book_appointment_by_user_id'),
    path('api/user/', UserCreateAPIView.as_view(), name='user-create'),
    # path('payments/', include('payments.urls'))
]
