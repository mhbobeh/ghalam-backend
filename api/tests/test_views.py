from re import T
import pytest, random, factory
from api.models import CustomUser, Post
from api.tests.Factories import UserFactory, PostFactory, PostLikeFactory
from django.test import TestCase, RequestFactory
from django.urls import reverse
from unittest.mock import patch
from rest_framework.test import APIClient
from faker import Faker
from django.utils.text import slugify
from django.db.models import signals


pytestmark = pytest.mark.django_db(databases=["default"])

@pytest.mark.django_db(databases=["default"])
class TestUser:
    databases = {"default"}
    pytestmark = pytest.mark.django_db(databases=["default"])
    
    faker = Faker()
    api_client = APIClient(HTTP_ACCEPT_LANGUAGE="en")

    def test_user_register(self):

        url = reverse("api:register")
        password = self.faker.password()
        data = {
            "username": self.faker.user_name(),
            "password": password,
            "password_repeat": password,
            "title": self.faker.sentence(),
            "full_name": self.faker.name(),
            "biography": self.faker.text(),
            "phone_number": f"0912{random.randint(1000000, 9999999)}"
        }
        resp = self.api_client.post(path=url, data=data)

        assert resp.data['data'] == 'user created successfully'
        assert resp.status_code == 200

    def test_wrong_phone_fail(self):

        url = reverse("api:register")
        password = self.faker.password()
        data = {
            "username": self.faker.user_name(),
            "password": password,
            "password_repeat": password,
            "title": self.faker.sentence(),
            "full_name": self.faker.name(),
            "biography": self.faker.text(),
            "phone_number": f"0812{random.randint(1000000, 9999999)}" #phone number must starts with 09
        }
        
        resp = self.api_client.post(path=url, data=data)
        
        assert resp.status_code != 200
        assert resp.status_code == 400

    def test_different_pass_fail(self):

        url = reverse("api:register")
        password = self.faker.password()
        data = {
            "username": self.faker.user_name(),
            "password": f"{password}",
            "password_repeat": f"{password}1",
            "title": self.faker.sentence(),
            "full_name": self.faker.name(),
            "biography": self.faker.text(),
            "phone_number": f"0912{random.randint(1000000, 9999999)}"
        }
        resp = self.api_client.post(path=url, data=data)
    
        assert resp.status_code != 200
        assert resp.status_code == 400

@pytest.mark.django_db(databases=["default"])
class TestPost:
    databases = {"default"}
    pytestmark = pytest.mark.django_db(databases=["default"])
    
    faker = Faker()

    def test_create_new_post(self, user_obj, auth_client):
        url = reverse("api:post-list")
        data = {
            "title": self.faker.sentence(),
            "text": self.faker.text(),
            "category": random.choice(Post.TYPE_CHOICES)[0],
        }
        resp = auth_client.post(path=url, data=data)

        assert resp.status_code == 201
        assert resp.data["title"] == data["title"]
        assert resp.data["slug"] == slugify(data["title"])
        assert resp.data["text"] == data["text"]
        assert resp.data["category"] == data["category"]
        assert resp.data["author"] == user_obj.id

    def test_anonymous_user_fail(self):

        url = reverse("api:post-list")
        data = {
            "title": self.faker.sentence(),
            "text": self.faker.text(),
            "category": random.choice(Post.TYPE_CHOICES)[0],
        }
        api_client = APIClient()
        resp = api_client.post(path=url, data=data)

        assert resp.status_code == 401


@pytest.mark.django_db(databases=["default"])
class TestPostLike:
    databases = {"default"}
    pytestmark = pytest.mark.django_db(databases=["default"])
    
    faker = Faker()

    def test_post_like(self, user_obj, post_obj, auth_client):

        assert post_obj.likes_count == 0
        
        url = f"/api/post/{post_obj.slug}/like/"
        resp = auth_client.post(path=url)

        post_obj.refresh_from_db()

        assert resp.status_code == 201
        assert post_obj.likes_count == 1

    def test_delete_post_like_after_like(self, post_obj, auth_client):

        assert post_obj.likes_count == 0
        
        url = f"/api/post/{post_obj.slug}/like/"
        resp = auth_client.post(path=url)

        post_obj.refresh_from_db()
        assert resp.status_code == 201
        assert post_obj.likes_count == 1

        delete_resp = auth_client.delete(path=url)
        post_obj.refresh_from_db()

        assert post_obj.likes_count == 0
        assert delete_resp.status_code == 204

    def test_delete_fail_before_like(self, post_obj, auth_client):

        assert post_obj.likes_count == 0
        
        url = f"/api/post/{post_obj.slug}/like/"

        delete_resp = auth_client.delete(path=url)
        post_obj.refresh_from_db()

        assert post_obj.likes_count == 0
        assert delete_resp.status_code == 409
        