from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from crmify.settings import crmify_settings


@receiver(post_save, sender=crmify_settings.LEAD_MODEL)
def update_crm_lead(instance=None, created=None, **kwargs):
    print('instance {} being saved'.format(instance))


@receiver(post_delete, sender=crmify_settings.LEAD_MODEL)
def delete_crm_lead(instance=None, created=None, **kwargs):
    print('instance {} being deleted'.format(instance))
