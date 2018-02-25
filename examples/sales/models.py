from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    auth = models.OneToOneField(User, related_name='profile')

    address = models.CharField(max_length=200, null=True, blank=True, default=None)
    city = models.CharField(max_length=100, null=True, blank=True, default=None)
    state = models.CharField(max_length=50, null=True, blank=True, default=None)


class Subscripton(models.Model):
    TYPE_FREE = 'free'
    TYPE_PAID = 'paid'
    SUBSCRIPTION_TYPES = (
        (TYPE_FREE, TYPE_FREE),
        (TYPE_PAID, TYPE_PAID),
    )

    user = models.ForeignKey(UserProfile, related_name='subscriptions')

    type = models.CharField(max_length=50, choices=SUBSCRIPTION_TYPES, default=TYPE_FREE)

