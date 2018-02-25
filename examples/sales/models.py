from django.db import models
from django.contrib.auth.models import User
from crmify.mixins import LeadStatusMixin


class UserProfile(models.Model):
    auth = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)

    address = models.CharField(max_length=200, null=True, blank=True, default=None)
    city = models.CharField(max_length=100, null=True, blank=True, default=None)
    state = models.CharField(max_length=50, null=True, blank=True, default=None)


class Subscription(LeadStatusMixin, models.Model):
    TYPE_FREE = 'free'
    TYPE_PAID = 'paid'
    SUBSCRIPTION_TYPES = (
        (TYPE_FREE, TYPE_FREE),
        (TYPE_PAID, TYPE_PAID),
    )

    user = models.ForeignKey(UserProfile, related_name='subscriptions', on_delete=models.CASCADE)

    type = models.CharField(max_length=50, choices=SUBSCRIPTION_TYPES, default=TYPE_FREE)

    def lead_status(self):
        if not self.user.auth.is_active:
            return self.user, self.DEAD_LEAD
        elif self.type == self.TYPE_FREE:
            return self.user, self.NEW_LEAD
        elif self.type == self.TYPE_PAID:
            return self.user, self.CONVERTED_LEAD

        return None
