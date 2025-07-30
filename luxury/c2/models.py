from django.db import models

class Client(models.Model):
    uid = models.CharField(max_length=64, unique=True)
    ip_address = models.GenericIPAddressField()
    hostname = models.CharField(max_length=255)
    connected_at = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.hostname} ({self.ip_address})"

class CommandLog(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    command = models.TextField()
    output = models.TextField(blank=True, null=True)
    executed_at = models.DateTimeField(auto_now_add=True)
