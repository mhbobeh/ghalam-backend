import pytest
from api.models import CustomUser, Post, PostLike
from api.tests.Factories import UserFactory, PostFactory, PostLikeFactory
from django.utils.text import slugify


pytestmark = pytest.mark.django_db(databases=['default'])

@pytest.mark.django_db(databases=['default'])
class TestUser:
    databases = {'default'}
    pytestmark = pytest.mark.django_db(databases=['default'])

    def test_init(self, user_obj):
        assert isinstance(user_obj, CustomUser)
    
    def test_user_params(self, user_obj):
        user = CustomUser.objects.get(id=user_obj.id)

        assert user.username == UserFactory.username
        assert user.full_name == UserFactory.full_name
        assert user.phone_number == UserFactory.phone_number
        assert user.title == UserFactory.title
        assert user.biography == UserFactory.biography


@pytest.mark.django_db(databases=['default'])
class TestPost:
    databases = {'default'}
    pytestmark = pytest.mark.django_db(databases=['default'])

    def test_init(self, post_obj):
        assert isinstance(post_obj, Post)
        assert isinstance(post_obj.author, CustomUser)
    
    def test_post_params(self, post_obj):
        post = Post.objects.get(id=post_obj.id)

        assert post.title == PostFactory.title
        assert post.slug == slugify(PostFactory.title)
        assert post.text == PostFactory.text
        assert post.category == PostFactory.category
        assert post.author == PostFactory.author.get_factory().create() #author is a subfactory, we should create an object to check it.
        

@pytest.mark.django_db(databases=['default'])
class TestPostLike:
    databases = {'default'}
    pytestmark = pytest.mark.django_db(databases=['default'])

    def test_init(self, post_like_obj):
        assert isinstance(post_like_obj, PostLike)
        assert isinstance(post_like_obj.user, CustomUser)
        assert isinstance(post_like_obj.post, Post)

    def test_post_like_params(self, post_like_obj):
        post_like = PostLike.objects.get(id=post_like_obj.id)

        assert post_like.user == PostLikeFactory.user.get_factory().create()
        assert post_like.post == PostLikeFactory.post.get_factory().create()
                