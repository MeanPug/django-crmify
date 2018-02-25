from django.db import models
from django.utils.timezone import now
from crmify.settings import crmify_settings
from crmify.backends import crm_backend
import logging

logger = logging.getLogger(__name__)


class CRMObject(models.Model):
    class Meta:
        abstract = True


class Lead(CRMObject):
    anchor = models.OneToOneField(crmify_settings.LEAD_MODEL, related_name='crm_lead', on_delete=models.CASCADE)

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
    external_status = models.CharField(max_length=200, null=True, blank=True, default=None)
    last_synced = models.DateTimeField(null=True, blank=True, default=None)

    def sync_to_crm(self):
        logger.debug('now syncing lead to CRM')

        self.external_id = crm_backend.sync_lead(self)
        self.last_synced = now()

        return self.external_id

    def delete_from_crm(self):
        logger.debug('now deleting lead from CRM')
        crm_backend.delete_lead(self.external_id)

    def __str__(self):
        return """{} -- {} {} // {} ({})""".format(
            self.email, self.first_name, self.last_name, self.external_id, self.id
        )
