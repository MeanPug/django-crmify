from crmify.backends.base import CRMBackend
from crmify.mixins import FieldMapperMixin
from crmify.lib.insightly import Insightly as InsightlyAPI
import logging

logger = logging.getLogger(__name__)


class InsightlyBackend(FieldMapperMixin, CRMBackend):
    api_version = 'v2.2'
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
        self._lead_statuses = None

    @property
    def connection(self):
        if self._connection:
            return self._connection

        self._connection = InsightlyAPI(api_key=self._auth_params['API_KEY'], version=self.api_version)
        return self._connection

    @property
    def lead_statuses(self):
        if self._lead_statuses:
            return self._lead_statuses

        self._lead_statuses = self.connection.read('leadstatuses', params={'include_converted': True})
        return self._lead_statuses

    def sync_lead(self, lead):
        crm_fields = self.apply_field_mapping(lead)

        if lead.external_status:
            # we have to extract the status ID of the status set on the lead
            try:
                crm_fields['lead_status_id'] = [l for l in self.lead_statuses if l['LEAD_STATUS'] == lead.external_status][0]['LEAD_STATUS_ID']
            except IndexError:
                raise ValueError('status {} isnt a valid lead status, correction required'.format(lead.external_status))

        if not lead.external_id:
            crm_fields.pop('lead_id')
            lead = self.connection.create('leads', crm_fields)
        else:
            lead = self.connection.update('leads', crm_fields)

        return lead['LEAD_ID']

    def delete_lead(self, lead_id):
        success = self.connection.delete('leads', id=lead_id)
        return success