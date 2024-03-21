# In your app's admin.py file
from django.contrib import admin
from .models import BookAppointment


class BookAppointmentAdmin(admin.ModelAdmin):
    def full_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    list_display = ('user', 'full_user_name', 'date_time', 'location')
    search_fields = ('user__username', 'location')


admin.site.register(BookAppointment, BookAppointmentAdmin)
