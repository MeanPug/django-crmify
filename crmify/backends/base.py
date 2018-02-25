class CRMBackend(object):
    def __init__(self, **auth_params):
        # for a variable like 'CRMIFY_BACKEND_AUTH_API_KEY', strip the CRMIFY_BACKEND_AUTH_ bit off
        self._auth_params = {k.replace('CRMIFY_BACKEND_AUTH_', ''): v for k, v in auth_params.items()}

    def sync_lead(self, lead):
        raise NotImplementedError

    def delete_lead(self, lead_id):
        raise NotImplementedError
