from django.contrib import admin

from core.models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    search_fields = ('id', 'uuid', 'user__uuid', 'user__id', 'user__username', 'user__email')
    list_display = ('id', 'uuid', 'scheduled', 'day', 'sms_received', 'attended')
    list_filter = ('attended', 'scheduled', 'day')
    raw_id_fields = ('user',)
