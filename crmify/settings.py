""" Ripped from the django-rest-framework settings.py

Settings for CRMIFY library are all namespaced in the CRMIFY setting.
For example your project's `settings.py` file might look like this:

CRMIFY = {
    'BACKEND': 'crmify.backends.insightly.InsightlyBackend',
    'BACKEND_OPTIONS': {
        'LEAD_NEW_STATUS': '',
        'LEAD_DEAD_STATUS': ''
    }
}

This module provides the `crmify_settings` object, that is used to access
CRMIFY framework settings, checking for user settings first, then falling
back to the defaults.
"""
from __future__ import unicode_literals

from importlib import import_module

from django.conf import settings
from django.test.signals import setting_changed
from django.utils import six
import os


auth_keys = ['API_KEY', 'USERNAME', 'PASSWORD']

DEFAULTS = {
    'BACKEND': 'crmify.backends.insightly.InsightlyBackend',
    'BACKEND_AUTH': {k: os.environ.get('CRMIFY_BACKEND_AUTH_{}'.format(k)) for k in auth_keys},
    'LEAD_MODEL': 'django.contrib.auth.models.User',
    'LEAD_MODEL_FIELDMAPPER': 'crmify.mappers.DjangoUserFieldMapper',
    'LEAD_STATUS_MODEL': None,
    'LEAD_NEW_STATUS': 'NotContacted',
    'LEAD_CONVERTED_STATUS': 'Converted',
    'LEAD_DEAD_STATUS': 'Disqualified'
}


# List of settings that may be in string import notation.
IMPORT_STRINGS = (
    'BACKEND',
    'LEAD_MODEL_FIELDMAPPER',
    'LEAD_MODEL',
    'LEAD_STATUS_MODEL',
)


def perform_import(val, setting_name):
    """
    If the given setting is a string import notation,
    then perform the necessary import or imports.
    """
    if val is None:
        return None
    elif isinstance(val, six.string_types):
        return import_from_string(val, setting_name)
    elif isinstance(val, (list, tuple)):
        return [import_from_string(item, setting_name) for item in val]
    return val


def import_from_string(val, setting_name):
    """
    Attempt to import a class from a string representation.
    """
    try:
        # Nod to tastypie's use of importlib.
        module_path, class_name = val.rsplit('.', 1)
        module = import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        msg = "Could not import '%s' for API setting '%s'. %s: %s." % (val, setting_name, e.__class__.__name__, e)
        raise ImportError(msg)


class APISettings(object):
    """
    A settings object, that allows API settings to be accessed as properties.
    For example:

        from crmify.settings import crmify_settings
        print(crmify_settings.BACKEND)

    Any setting with string import paths will be automatically resolved
    and return the class, rather than the string literal.
    """
    def __init__(self, user_settings=None, defaults=None, import_strings=None):
        if user_settings:
            self._user_settings = self.__check_user_settings(user_settings)
        self.defaults = defaults or DEFAULTS
        self.import_strings = import_strings or IMPORT_STRINGS
        self._cached_attrs = set()

    @property
    def user_settings(self):
        if not hasattr(self, '_user_settings'):
            self._user_settings = getattr(settings, 'CRMIFY', {})
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid API setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Coerce import strings into classes
        if attr in self.import_strings:
            val = perform_import(val, attr)

        # Cache the result
        self._cached_attrs.add(attr)
        setattr(self, attr, val)
        return val

    def __check_user_settings(self, user_settings):
        return user_settings

    def reload(self):
        for attr in self._cached_attrs:
            delattr(self, attr)
        self._cached_attrs.clear()
        if hasattr(self, '_user_settings'):
            delattr(self, '_user_settings')


crmify_settings = APISettings(None, DEFAULTS, IMPORT_STRINGS)


def reload_crmify_settings(*args, **kwargs):
    setting = kwargs['setting']

    if setting == 'CRMIFY':
        crmify_settings.reload()


setting_changed.connect(reload_crmify_settings)