from django.urls import path, include
from api.views import (ProfileView,
                       UserView,
                       )
from rest_framework.routers import DefaultRouter


router = DefaultRouter()


router.register(r'user', UserView, basename='user')

app_name = 'api'

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
] + router.urls 