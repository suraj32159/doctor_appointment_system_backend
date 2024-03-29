from django.contrib import admin
from django.utils.html import format_html
from .models import BookAppointment


class BookAppointmentAdmin(admin.ModelAdmin):
    def full_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def gmeet_link_clickable(self, obj):
        if obj.gmeet_link:
            return format_html('<a href="{0}" target="_blank">{0}</a>', obj.gmeet_link)
        return "No link provided"

    list_display = ('user', 'full_user_name', 'date_time', 'gmeet_link_clickable', 'contact_number', 'location')
    search_fields = ('user__username', 'location')


admin.site.register(BookAppointment, BookAppointmentAdmin)
