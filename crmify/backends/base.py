class CRMBackend(object):
    def __init__(self, **auth_params):
        self._auth_params = auth_params

    def authenticate(self, **auth_params):
        """ do any necessary authentication steps
        :param auth_params: `dict` packed of authentication parameters
        :return:
        """
        return None

    def create_lead(self, **lead_params):
        pass

    def update_lead(self, **update_params):
        pass
