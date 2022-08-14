from rest_framework import serializers
from api.models import CustomUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = '__all__'
        read_only_fields = ("date_joined", "last_login")
        extra_kwargs = {
            'password': {'write_only': True}
        }


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fiedls = (
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "phone_number"
            )

        read_only_fields = ('username',)
        extra_kwargs = {
            'password': {'write_only': True}
        }