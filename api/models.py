from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from persiantools.jdatetime import JalaliDate
import os



class CustomUser(AbstractUser):
    
    title = models.CharField(max_length=150)
    full_name = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=11, unique=True)
    biography = models.TextField(max_length=2000)

    def __str__(self):
        return self.title


def media_directory_path(instance, filename):
    today = JalaliDate.today()
    this_year = str(today.year)
    this_month = str(today.month)
    ext = filename.split('.')[-1]
    return os.path.join('media', this_year, this_month, instance.slug, f'{instance.slug[:20]}.{ext}')