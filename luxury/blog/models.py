from django.db import models
from datetime import datetime

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=150)
    body = models.CharField(max_length=1000000)
    category = models.CharField(max_length=30, null=True)
    image = models.ImageField(upload_to='blogImages', null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)