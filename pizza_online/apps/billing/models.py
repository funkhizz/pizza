from django.db import models
from pizza_online.apps.users.models import User, GuestUser
from django.dispatch import receiver
from django.db.models.signals import post_save


class BillingProfileManager(models.Manager):
    def new_or_get(self, request):
        user = request.user
        email = request.session.get("email_id")
        created = False
        obj = None
        if user.is_authenticated:
            obj, created = self.model.objects.get_or_create(user=user, email=user)
        else:
            guest_email = GuestUser.objects.create(email=email)
            guest_email_obj, guest_email_obj_created = GuestUser.objects.get_or_create(
                id=guest_email.id
            )
            obj = self.model.objects.create(email=guest_email_obj)
        return obj, created


class BillingProfile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    email = models.EmailField(null=True, blank=True)
    active = models.BooleanField(default=True)
    update = models.DateField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = BillingProfileManager()

    def __str__(self):
        return self.email


@receiver(post_save, sender=User)
def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)
