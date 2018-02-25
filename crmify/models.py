from django.db import models


class CRMObject(models.Model):
    class Meta:
        abstract = True


class Lead(CRMObject):
    lead_source = models.CharField(max_length=100, null=True, blank=True, default=None)

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=200, null=True, blank=True, default=None)
    secondary_email = models.CharField(max_length=200, null=True, blank=True, default=None)
    phone = models.CharField(max_length=50, null=True, blank=True, default=None)
    mobile_phone = models.CharField(max_length=50, null=True, blank=True, default=None)
    dob = models.DateField(max_length=50, null=True, blank=True, default=None)

    street_address = models.CharField(max_length=200, null=True, blank=True, default=None)
    city = models.CharField(max_length=200, null=True, blank=True, default=None)
    state = models.CharField(max_length=50, null=True, blank=True, default=None)
    country = models.CharField(max_length=50, null=True, blank=True, default=None)

    external_id = models.CharField(max_length=200, unique=True)
