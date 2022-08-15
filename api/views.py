from django.shortcuts import render
from rest_framework import viewsets, generics, permissions, views, status, filters
from api.models import CustomUser, Post, PostLike
from api.serializers import (ProfileSerializer,
                             UserSerializer,
                             RegisterSerializer,
                             SendOTPSerializer,
                             VerifyOTPSerializer,
                             ForgetPasswordSerializer,
                             ChangePasswordSerializer,
                             PostSerializer,
                             FavouriteCategorySerializer
                             )
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from api.tasks import send_otp
from api.services import OTPManager, UUIDManager
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend




class UserView(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    

class ProfileView(generics.RetrieveUpdateAPIView):
    permissions_classes = (permissions.IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_object(self):
        return get_object_or_404(CustomUser, id=self.request.user.id)


class RegisterView(views.APIView):

    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        CustomUser.objects.create_user(**serializer.validated_data)
        return Response(data={'data':_('user created successfully')}, status=status.HTTP_200_OK)



class SendOTPView(views.APIView):

    @swagger_auto_schema(request_body=SendOTPSerializer)    
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer._validated_data
        send_otp(data['phone_number'])
        return Response(status=status.HTTP_200_OK)


class VerifyOTPView(views.APIView):

    @swagger_auto_schema(request_body=VerifyOTPSerializer)
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        otp = OTPManager(data['phone_number'])
        if otp.is_valid(data['otp']):
            uuid = UUIDManager(data['phone_number'])
            uuid.generate_save()
            return Response(data={'data': _({'recovery_code': uuid.value})}, status=status.HTTP_200_OK)

        return Response(data={'detail': _('wrong phone number or OTP')}, status=status.HTTP_401_UNAUTHORIZED)                                                                                                                                                    
 

class ForgetPasswordView(views.APIView):

    @swagger_auto_schema(request_body=ForgetPasswordSerializer)
    def post(self, request):
        serializer = ForgetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        User = get_user_model()
        uuid = UUIDManager(data['phone_number'])
        if uuid.is_valid(data['tracking_code']):
            user = get_object_or_404(User, phone_number=data['phone_number'])
            user.set_password(data['password'])
            user.save()
            return Response(status=status.HTTP_200_OK)

        return Response(data={'detail': _('wrong phone number or OTP')}, status=status.HTTP_401_UNAUTHORIZED)


class ChangePasswordView(views.APIView):

    permission_classes =(IsAuthenticated, )

    @swagger_auto_schema(request_body=ChangePasswordSerializer)
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if self.request.user.check_password(data['current_password']):
            self.request.user.set_password(data['password'])
            self.request.user.save()
            data = {'detail': _('password reset successfully.')}
            return Response(data=data, status=status.HTTP_200_OK)

        data = {'detail': _('check if you entered current password correctly.')}
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)


class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly, )
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['category', ]
    ordering_fields = ['likes_count', 'views_count', 'created_at']
    search_fields = ['title', 'text', 'author__full_name']
    lookup_field = "slug"

    def retrieve(self, request, *args, **kwargs):
        post = self.get_object()
        post.views_count = post.views_count + 1
        post.save(update_fields=('views_count',))
        return super().retrieve(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



class PostLikeView(views.APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        user = request.user
        post = Post.objects.filter(slug=kwargs["slug"])
        post_like = PostLike.objects.filter(user_id=user.id, post_id=post.first().id)

        if post.exists():
            if not post_like.exists():
                PostLike.objects.create(user=user, post=post.first())
                return Response(status=status.HTTP_201_CREATED)

            return Response(status=status.HTTP_409_CONFLICT, data={"detail": _("you've already liked this photo")})

        return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": _("No Post Found")})

    def delete(self, request, *args, **kwargs):
        user = request.user
        post = Post.objects.filter(slug=kwargs["slug"])
        post_like = PostLike.objects.filter(user_id=user.id, post_id=post.first().id)

        if post.exists():
            if post_like.exists():
                post_like.first().delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

            return Response(status=status.HTTP_409_CONFLICT, data={"detail": _("you haven't liked this photo")})

        return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": _("No Post Found")})


class FavouriteCategory(views.APIView):

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = FavouriteCategorySerializer
        serializer.is_valid(raise_exception=True)


        data = {
            "user": user,
            "category": serializer.validated_data["category"]
        }
        favorite_category = FavouriteCategory.objects.filter(**data)

        if not favorite_category.exists():
            FavouriteCategory.objects.create(**data)
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_409_CONFLICT, data={"detail": _("you've already selected this category")})

    def delete(self, request, *args, **kwargs):
        user = request.user
        serializer = FavouriteCategorySerializer
        serializer.is_valid(raise_exception=True)

        data = {
            "user": user,
            "category": serializer.validated_data["category"]
        }
        favorite_category = FavouriteCategory.objects.filter(**data)

        if favorite_category.exists():
            favorite_category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_409_CONFLICT, data={"detail": _("you haven't selected this category before")})
