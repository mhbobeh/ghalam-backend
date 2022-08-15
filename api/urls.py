from django.urls import path, include
from api.views import (ProfileView,
                       UserView,
                       RegisterView,
                       SendOTPView,
                       VerifyOTPView,
                       ForgetPasswordView,
                       ChangePasswordView,
                       PostView,
                       PostLikeView,
                       FavouriteCategory
                       )
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = DefaultRouter()


router.register(r'user', UserView, basename='user')
router.register(r'post', PostView, basename='post')

app_name = 'api'

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('send-otp/', SendOTPView.as_view(), name='send_otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('forget-password/', ForgetPasswordView.as_view(), name='forget_password'),
    path('reset-password/', ChangePasswordView.as_view(), name='reset_password'),
    path('post/<slug:slug>/like/', PostLikeView.as_view(), name='post_like'),
    path('favorite_category/', FavouriteCategory.as_view(), name='favourite_category')
] + router.urls 