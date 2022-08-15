from os import environ
import random
import uuid
from django.core.cache import caches
from ghalam.environments import OTP_EXPIRE_TIME

class OTPManager:

    otp_cache = caches['password_otp']

    def __init__(self, phone_number):
        self.phone_number = phone_number

    def generate_save(self):
        self._otp = random.randint(10987, 987654)
        self.otp_cache.set(self.phone_number, self._otp, OTP_EXPIRE_TIME)

    def send(self):
        print(f"======OTP={self.value}=======")

    @property
    def value(self):
        return self.otp_cache.get(self.phone_number)

    def is_valid(self, otp):
        if str(self.otp_cache.get(self.phone_number)) == otp:
            self.otp_cache.delete(self.phone_number)
            return True
        return False

    def otp_ttl(self):
        return self.otp_redis.ttl(self.phone_number)

class UUIDManager:
    
    uuid_cache = caches['password_uuid']

    def __init__(self, phone_number):
        self.phone_number = phone_number

    def generate_save(self):
        self.uuid = uuid.uuid4().hex
        self.uuid_cache.set(self.phone_number, self.uuid)
        print(f'uuid: {self.uuid}')

    @property
    def value(self):
        return self.uuid_cache.get(self.phone_number)
    
    def is_valid(self, uuid):
        if self.uuid_cache.get(self.phone_number) == uuid:
            self.uuid_cache.delete(self.phone_number)
            return True
        return False