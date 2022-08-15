from django.db.models.signals import post_save
from django.dispatch import receiver
from api.models import Post, CustomUser
from api.tasks import send_mass_email
from django.urls import reverse






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