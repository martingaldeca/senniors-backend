from django.contrib import admin

from core.models import ClinicHistory


@admin.register(ClinicHistory)
class ClinicHistoryAdmin(admin.ModelAdmin):
    search_fields = ('id', 'uuid', 'user__uuid', 'user__id', 'user__username', 'user__email')
    list_display = ('id', 'uuid', 'scholarship', 'hypertension', 'diabetes', 'alcoholism', 'handicap')
    list_filter = ('scholarship', 'hypertension', 'diabetes', 'alcoholism', 'handicap')
    raw_id_fields = ('user',)
