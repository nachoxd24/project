# en signals.py

from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from .models import LoginCount

@receiver(user_logged_in)
def update_login_count(sender, user, **kwargs):
    login_count, created = LoginCount.objects.get_or_create(user=user)
    login_count.count += 1
    login_count.save()
