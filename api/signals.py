from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from api.models import Post, CustomUser, PostLike
from api.tasks import send_mass_email
from django.urls import reverse


@receiver(pre_save, sender=PostLike)
def increase_like(sender, instance, *args, **kwargs):
    instance.post.likes_count = instance.post.likes_count + 1
    instance.post.save()
        

@receiver(pre_delete, sender=PostLike)
def decrease_like(sender, instance, *args, **kwargs):
    instance.post.likes_count = instance.post.likes_count - 1
    instance.post.save()


@receiver(post_save, sender=Post)
def notify_users(sender, instance, created, *args, **kwargs):
    if created:
        users_emails = list(CustomUser.objects.filter(favourites__category=instance.category).values_list('email', flat=True))
        post_url = f"{reverse('api:post-list')}{instance.slug}/"

        send_mass_email(
            email_list=users_emails,
            subject=f"new post published on {instance.category} category.",
            message=f"""hi dear user\n there is a new post recently published on your favourite category: {instance.category}\n
            you can check it at {post_url}"""
        )