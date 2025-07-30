from django.contrib import admin
from .models import PhishingLog, KeystrokeLog, GeoLog, FingerprintLog, EvasionLog

admin.site.register(PhishingLog)
admin.site.register(KeystrokeLog)
admin.site.register(GeoLog)
# admin.site.register(FingerprintLog)
admin.site.register(EvasionLog)

@admin.register(FingerprintLog)
class FingerprintLogAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'device_type', 'platform', 'timestamp')
    list_filter = ('device_type', 'platform')
    search_fields = ('ip_address', 'user_agent')
    readonly_fields = ('timestamp', 'raw_data')