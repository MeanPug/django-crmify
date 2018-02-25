from crmify.settings import crmify_settings


class FieldMapperMixin(object):
    field_mapping = {}
    fallbacks = {}

    def lookup_value(self, field, instance):
        """ nested value lookup for the given field on the given instance. For example, 'auth__username'
        :param field: `str` field to lookup
        :param instance: `object` to lookup field on
        :return: `value`
        """
        parts = field.split('__')
        field_name = parts[0]
        remainder = '__'.join(parts[1:])

        if not remainder:
            return getattr(instance, field_name)
        else:
            return self.lookup_value(remainder, getattr(instance, field_name))

    def apply_field_mapping(self, instance):
        fieldset = {}

        # model field, lead field
        for mfield, lfield in self.field_mapping.items():
            fieldset[lfield] = self.lookup_value(mfield, instance)

        for mfield, lfield in self.fallbacks.items():
            if fieldset.get(lfield) is None:
                fieldset[lfield] = self.lookup_value(mfield, instance)

        return fieldset


class LeadStatusMixin(object):
    """ subclasses of this Mixin should implement the single `lead_status` method. The result of this method will
    be used to signal lifecycle events in the Lead, which are then synced to the CRM
    """
    NEW_LEAD = crmify_settings.LEAD_NEW_STATUS
    CONVERTED_LEAD = crmify_settings.LEAD_CONVERTED_STATUS
    DEAD_LEAD = crmify_settings.LEAD_DEAD_STATUS

    def lead_status(self):
        raise NotImplementedError('to track lead statuses, you should implement the lead_status method')