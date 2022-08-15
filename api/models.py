from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from persiantools.jdatetime import JalaliDate
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import timedelta
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


class Post(models.Model):

    SOCIAL = 'Social'
    ECONOMY = 'Economy'
    POLITIC = 'Politic'
    SPORT = 'Sport'
    COMEDY = 'Comedy'
    OTHER = 'Other'

    TYPE_CHOICES = (
        (SOCIAL, _('social')), (ECONOMY, _('economy')), (POLITIC,_('politic')), 
        (SPORT, _('sport')), (COMEDY, _('comedy')), (OTHER, _('other')))
        
    title = models.CharField(max_length=300)
    slug = models.SlugField(allow_unicode=True, unique=True, blank=True)
    text = models.TextField(max_length=5000)

    category = models.CharField(
        max_length=200,
        choices=TYPE_CHOICES
        )

    image = models.ImageField(
        upload_to=media_directory_path, 
        blank=True
        )

    video = models.FileField(
        upload_to=media_directory_path,
        blank=True
        )

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='posts'
        )

    likes_count = models.IntegerField(default=0)
    views_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_published_recently(self):
        return self.created_at > timezone.now() - timedelta(days=1)
    
    @property
    def is_moodified_recently(self):
        return self.updated_at > timezone.now() - timedelta(days=1)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class PostLike(models.Model):

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='post_likes'
        )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes'
        )


class FavouriteCategory(models.Model):

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='favourites'
        )

    category = models.CharField(
        max_length=200,
        choices=Post.TYPE_CHOICES,
        null=True,
        blank=True
        )
