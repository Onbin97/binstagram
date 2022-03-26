from django.db import models

from utils.models import TimestampZone

class User(TimestampZone):
    name         = models.CharField(max_length=200)
    email        = models.CharField(max_length=200, unique=True)
    password     = models.CharField(max_length=2000)
    phone_number = models.CharField(max_length=200)
    
    class Meta:
        db_table = "users"