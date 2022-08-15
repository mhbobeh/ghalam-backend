import pytest, factory
from api.tests.Factories import UserFactory, PostFactory, PostLikeFactory
from pytest_factoryboy import register
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient
from django.db.models import signals


register(UserFactory)
register(PostFactory)
register(PostLikeFactory)

@pytest.fixture
def user_obj(db, user_factory): # pass db parameter to grant database access.
    user = user_factory.create()
    return user


@pytest.fixture
def auth_client(db, user_obj):
    api_client = APIClient(HTTP_ACCEPT_LANGUAGE="en")
    refresh = RefreshToken.for_user(user_obj)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return api_client


@pytest.fixture
@factory.django.mute_signals(signals.post_save)
def post_obj(db, post_factory):
    post = post_factory.create()
    return post

@pytest.fixture
@factory.django.mute_signals(signals.post_save)
def post_like_obj(db, post_like_factory):
    post_like = post_like_factory.create() # ==> save to db
    return post_like


@pytest.fixture
def unsaved_post_like_obj(db, post_like_factory):
    post_like = post_like_factory.build() # ==> doesn't save to db
    return post_like
    