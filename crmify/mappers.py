from crmify.models import Lead


class FieldMapper(object):
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

    def create_lead(self, instance):
        """ create a `Lead` object from the given object instance (an instance of the class given by settings.LEAD_MODEL)
        :param instance: `object` of class settings.LEAD_MODEL
        :return: `Lead` instance, as created from the given instance
        """
        lead_fields = self.apply_field_mapping(instance)
        lead_fields['anchor'] = instance
        return Lead.objects.create(**lead_fields)

    def update_lead(self, lead, instance):
        """ updates a `Lead` object from the given object instance
        :param lead: `Lead` instance to update
        :param instance: `object` of class settings.LEAD_MODEL
        :return: `Lead` instance as updated by the given instance
        """
        lead_fields = self.apply_field_mapping(instance)

        for f, val in lead_fields.items():
            setattr(lead, f, val)

        lead.save()

        return lead


class DjangoUserFieldMapper(FieldMapper):
    field_mapping = {
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'email',
    }
    fallbacks = {
        'username': 'email'
    }