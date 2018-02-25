from crmify.settings import crmify_settings
import os


def get_backend():
    backend_cls = crmify_settings.BACKEND
    return backend_cls(**crmify_settings.BACKEND_AUTH)


crm_backend = get_backend()