from django.shortcuts import render
from rest_framework import viewsets, generics, permissions
from api.models import CustomUser
from api.serializers import (ProfileSerializer,
                             UserSerializer,
)
from django.shortcuts import get_object_or_404




class UserView(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    

class ProfileView(generics.RetrieveUpdateAPIView):
    permissions_classes = (permissions.IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_object(self):
        return get_object_or_404(CustomUser, id=self.request.user.id)