from django.db import models
from django.contrib.auth.models import User, Group


class AuthenticationRequest(models.Model):
    """
    Represents an Aunthentication Request. This is a request put in when a new
    user registers. A new user is not given all the permissions of the group
    when they registerd. Instead, they have to be manually given permissions
    by existing members. This class houses the requests for those permissions
    """

    user = models.ForiegnKey(User, null=True)
    group = models.ForiegnKey(Group, null=True)
    request_date = models.DateField(null=True)
    is_approved = models.BooleanField(default=False)
