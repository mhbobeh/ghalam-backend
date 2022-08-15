from rest_framework import serializers
from api.models import CustomUser
from django.utils.translation import gettext_lazy as _


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


class ValidPhoneSerializer(serializers.Serializer):

    def validate_phone_number(self, value):
        if value.startswith('09') and value.isnumeric():
            return value
        raise serializers.ValidationError(_("phone number must starts with '09' and contians 11 digits."))


class SamePassSerializer(serializers.Serializer):

    def validate(self, attrs):
        if attrs['password'] == attrs['password_repeat']:
            attrs.pop('password_repeat')
            return attrs
        raise serializers.ValidationError(_('passwords does not match'))


class RegisterSerializer(SamePassSerializer, ValidPhoneSerializer, serializers.ModelSerializer):
    password_repeat = serializers.CharField(max_length=128)
    class Meta:
        model = CustomUser
        fields = ('username', 
                  'password',
                  'password_repeat',
                  'title',
                  'biography',
                  'full_name',
                  'phone_number',
                  'email',)
        read_only_fields = ("date_joined", "last_login")
        extra_kwargs = {
            'password': {'write_only': True},
            'password_repeat': {'write_only': True},
        }


class SendOTPSerializer(ValidPhoneSerializer):
    phone_number = serializers.CharField()


class VerifyOTPSerializer(ValidPhoneSerializer):
    phone_number = serializers.CharField()
    otp = serializers.CharField(max_length=6)


class ForgetPasswordSerializer(SamePassSerializer, ValidPhoneSerializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(max_length=128)
    password_repeat = serializers.CharField(max_length=128)
    recovery_code = serializers.CharField()