from api.models import CustomUser, Post, PostLike
import factory, random
from faker import Faker


fake = Faker()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser
        django_get_or_create = ('username', )

    username = 'test_user_2000'
    full_name = fake.name()
    phone_number = f'09{random.randint(100000000, 999999999)}'
    title = 'Front-End Developer'
    biography = fake.text()


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post
        django_get_or_create = ('title', 'text', 'category', 'author')

    title = fake.name() #use name to have short title & slug
    text = fake.text()
    category = random.choice(Meta.model.TYPE_CHOICES)[0]
    author = factory.SubFactory(UserFactory)


class PostLikeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PostLike
        django_get_or_create = ('user', 'post')
    
    user = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)
