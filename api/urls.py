from django.urls import path, include
from api.views import (ProfileView,
                       UserView,
                       RegisterView,
                       SendOTPView,
                       VerifyOTPView,
                       ForgetPasswordView
                       )
from rest_framework.routers import DefaultRouter


router = DefaultRouter()


router.register(r'user', UserView, basename='user')

app_name = 'api'

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('send-otp/', SendOTPView.as_view(), name='send_otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('forget-password/', ForgetPasswordView.as_view(), name='forget_password'),
] + router.urls 