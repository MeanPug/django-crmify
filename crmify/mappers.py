from crmify.mixins import FieldMapperMixin


class LeadModelFieldMapper(FieldMapperMixin):
    """ a LeadModelFieldMapper is a FieldMapper which specifically knows how to transform the fields of settings.LEAD_MODEL
    into a Lead object
    """
    def create_lead(self, instance):
        """ create a `Lead` object from the given object instance (an instance of the class given by settings.LEAD_MODEL)
        :param instance: `object` of class settings.LEAD_MODEL
        :return: `Lead` instance, as created from the given instance
        """
        from crmify.models import Lead

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


class DjangoUserFieldMapper(LeadModelFieldMapper):
    field_mapping = {
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'email',
    }
    fallbacks = {
        'username': 'email'
    }

