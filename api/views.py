from django.shortcuts import render
from rest_framework import viewsets, generics, permissions, views, status
from api.models import CustomUser
from api.serializers import (ProfileSerializer,
                             UserSerializer,
                             RegisterSerializer,
)
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _




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