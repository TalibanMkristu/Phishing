from django.contrib import admin
from .models import PhishingLog, KeystrokeLog, GeoLog, FingerprintLog, EvasionLog

admin.site.register(PhishingLog)
admin.site.register(KeystrokeLog)
admin.site.register(GeoLog)
admin.site.register(FingerprintLog)
admin.site.register(EvasionLog)
