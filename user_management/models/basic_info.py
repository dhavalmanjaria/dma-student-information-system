from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
import hashlib
import datetime


class BasicInfo(models.Model):
    """
    This model stores basic information available required for all users
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    contact_number = models.CharField(
        help_text='The contact number of the user',
        blank=True,
        max_length=10)

    #TODO: Figure out how to get a hash of the email,
    def _get_hash():
        m = hashlib.sha256()
        m.update(str(datetime.datetime.now()).encode())
        return m.hexdigest()[:6]

    serial_no = models.CharField(
        help_text='Simpler unique identifier for this user',
        max_length=6,
        unique=True)


# This is basic basic info HAS to be saved.
# We might not use signals when saving user info.


@receiver(post_save, sender=User)
def create_basic_info(sender, instance, created, **kwargs):
    if created:
        BasicInfo.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_basic_info(sender, instance, **kwargs):
    instance.basicinfo.serial_no = BasicInfo._get_hash()
    instance.basicinfo.save()


