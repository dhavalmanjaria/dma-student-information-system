from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Permission, Group
from django.contrib.auth.hashers import make_password
import logging

LOG = logging.getLogger('app')


class Command(BaseCommand):
    """
    This command creates a default Upper Management user (since it is
    supposed to have all permissions).
    This is generally for trial purposes.
    """
    def handle(self, *args, **options):
        um0, created = User.objects.get_or_create(username='um0')
        um0.password = make_password('dhaval27')

        umg = Group.objects.get(name='UpperManagement')
        um0.groups.add(Group.objects.get(name='UpperManagement'))
        um0.basicinfo.group = umg
        um0.first_name = "UM"
        um0.last_name = "User"
        perms = umg.permissions.all()
        um0.user_permissions.set(perms)

        um0.save()
