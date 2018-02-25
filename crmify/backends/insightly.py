from crmify.backends.base import CRMBackend
from crmify.mappers import FieldMapperMixin
from crmify.lib.insightly import Insightly as InsightlyAPI
import logging

logger = logging.getLogger(__name__)


class InsightlyBackend(FieldMapperMixin, CRMBackend):
    api_version = '2.2'
    field_mapping = {
        'external_id': 'lead_id',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'email_address',
        'phone': 'phone_number',
        'mobile_phone': 'mobile_phone_number',
        'street_address': 'address_street',
        'city': 'address_city',
        'state': 'address_state',
        'country': 'address_country',
    }

    def __init__(self, *args, **kwargs):
        super(InsightlyBackend, self).__init__(**kwargs)
        self._connection = None

    @property
    def connection(self):
        if self._connection:
            return self._connection

        self._connection = InsightlyAPI(apikey=self._auth_params['API_KEY'], version=self.api_version)
        return self._connection

    def sync_lead(self, lead):
        crm_fields = self.apply_field_mapping(lead)

        if not lead.external_id:
            crm_fields.pop('lead_id')
            lead = self.connection.create('leads', crm_fields)
        else:
            lead = self.connection.update('leads', crm_fields)

        return lead['LEAD_ID']

    def delete_lead(self, lead_id):
        success = self.connection.delete('leads', id=lead_id)
        return success